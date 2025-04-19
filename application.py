from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from projects_code.norm_mut_logic import run_norm_mut_test
from tesla_api_backend.db import connect
import json
import os
from dotenv import load_dotenv
from datetime import datetime

application = Flask(__name__)
CORS(application)
load_dotenv()

WATCHER_SERVER = "http://18.224.68.167:8000"
application.config['TEMPLATES_AUTO_RELOAD'] = True


def render_page(template):
    """Serve full page normally, or just content for AJAX requests"""
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template(template)
    return render_template(template)


@application.route('/')
def home():
    return render_page("index.html")


@application.route('/projects')
def projects():
    return render_page("projects.html")


@application.route('/about')
def about():
    return render_page("about.html")


@application.route('/contact')
def contact():
    return render_page("contact.html")


@application.route('/norm-mut-test', methods=["GET", "POST"])
def norm_mut_test():
    if request.method == "POST":
        test_cases = request.json.get("test_cases", [])
        results = run_norm_mut_test(test_cases)
        return jsonify(results)
    return render_page("norm-mut-test.html")


@application.route("/task-manager/task-manager-login")
def task_manager_login():
    return render_page("task-manager/task-manager-login.html")


@application.route("/task-manager/register")
def task_manager_register():
    return render_page("task-manager/register.html")


@application.route("/task-manager/tasks")
def task_manager_tasks():
    return render_page("task-manager/tasks.html")


@application.route("/certifications")
def certifications():
    return render_page("certifications.html")


@application.route("/tesla")
def tesla():
    return render_page("tesla.html")

@application.route("/api/status")
def api_status():
    try:
        filepath = "/home/ec2-user/TeslaCharging/cached_vehicle_data.json"

        with open(filepath) as f:
            data = json.load(f)

        charge = data["charge_state"]

        last_modified_timestamp = os.path.getmtime(filepath)
        last_modified = datetime.fromtimestamp(last_modified_timestamp).isoformat()

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


@application.route("/api/recent-events")
def api_recent_events():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT timestamp, battery_level, energy_added, charging_state, event_type 
                    FROM charge_log 
                    ORDER BY timestamp DESC 
                    LIMIT 10;
                """)
                rows = cur.fetchall()

        events = []
        for row in rows:
            events.append({
                "timestamp": row[0],
                "battery_level": row[1],
                "energy_added": row[2],
                "charging_state": row[3],
                "event_type": row[4]
            })

        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)
