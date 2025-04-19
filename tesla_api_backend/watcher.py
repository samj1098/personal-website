import time
import os
import json
from datetime import datetime
from flask import Flask, jsonify
from tesla_client import get_vehicle_data, save_to_cache
from db import log_charge_data

POLL_INTERVAL = 60  # seconds
CACHE_PATH = "tesla_api_backend/cached_vehicle_data.json"
CACHE_INTERVAL = 300  # 5 minutes

app = Flask(__name__)
CORS(app)

@app.route("/api/status")
def api_status():
    try:
        with open(CACHE_PATH) as f:
            data = json.load(f)

        charge = data["charge_state"]
        last_modified = datetime.fromtimestamp(os.path.getmtime(CACHE_PATH)).isoformat()

        return jsonify({
            "battery_level": charge["battery_level"],
            "charging_state": charge["charging_state"],
            "charge_rate": charge["charge_rate"],
            "energy_added": charge["charge_energy_added"],
            "estimated_range": charge["battery_range"],
            "is_live": True,
            "last_updated": last_modified
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def watch_for_charge_end():
    print("Watching for unplug events...")
    last_charging_state = None
    last_battery_level = None
    last_odometer = None
    last_shift_state = None

    while True:
        try:
            data, is_live = get_vehicle_data()

            if not is_live:
                print("Vehicle asleep — skipping.")
                time.sleep(POLL_INTERVAL)
                continue

            #Check if we should save the snapshot
            try:
                last_modified = os.path.getmtime(CACHE_PATH)
                seconds_since_update = time.time() - last_modified
            except FileNotFoundError:
                seconds_since_update = float('inf')

            if seconds_since_update >= CACHE_INTERVAL:
                print("Saving snapshot to cache (no previous file found)")
                save_to_cache(data)

            charge = data['charge_state']
            vehicle_state = data['vehicle_state']
            drive_state = data['drive_state']

            charging_state = charge['charging_state']
            battery_level = charge['battery_level']
            odometer = vehicle_state['odometer']
            shift_state = drive_state['shift_state']

            print(f"Vehicle online, Charging: {charging_state}")

            # 1. Detect CHARGE event
            if last_charging_state == "Charging" and charging_state != "Charging":
                print("⚡️ Charge session ended — saving data.")
                log_charge_data(data, "charge")

            # 2. Drive Session End Detection (on park)
            if (
                last_shift_state is not None
                and last_shift_state in ["D", "R", "N"]
                and shift_state is None
                and last_odometer is not None
                and odometer > last_odometer
            ):
                print("🚗 Drive completed — logging drive event.")
                log_charge_data(data, "drive")

            # 3. Detect IDLE battery drain
            battery_drop = last_battery_level - battery_level if last_battery_level is not None else 0
            drove = (last_odometer is not None and odometer > last_odometer)

            if not drove and battery_drop >= 1:
                print("🪫 Idle drain detected — logging idle event.")
                log_charge_data(data, "idle")

            last_charging_state = charging_state
            last_odometer = odometer
            last_battery_level = battery_level
            last_shift_state = shift_state

            time.sleep(POLL_INTERVAL)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    import threading

    # Thread 1: background data collection
    t1 = threading.Thread(target=watch_for_charge_end)
    t1.daemon = True
    t1.start()

    # Thread 2: run Flask API server
    app.run(host="0.0.0.0", port=8000)