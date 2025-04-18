import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

#connection with PostgreSQL
def connect():
    return psycopg2.connect(DB_URL)

def create_table():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS charge_log (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    battery_level INTEGER,
                    charging_state TEXT,
                    charge_rate FLOAT,
                    energy_added FLOAT,
                    est_range FLOAT
                );
            """)
            conn.commit()

def log_charge_data(data, event_type):
    charge = data['charge_state']
    battery_level = charge['battery_level']
    energy_added = charge['charge_energy_added']

    with connect() as conn:
        with conn.cursor() as cur:
            # Get most recent entry
            cur.execute("""
                SELECT battery_level, energy_added 
                FROM charge_log 
                ORDER BY timestamp DESC 
                LIMIT 1;
            """)
            last = cur.fetchone()

            if last:
                last_battery, last_energy = last
                battery_diff = abs(last_battery - battery_level)
                energy_diff = abs(last_energy - energy_added)

                if battery_diff <= 1 and energy_diff <= 0.1:
                    print("⏱ No significant change — skipping log.")
                    return

            # Log new session
            cur.execute("""
                INSERT INTO charge_log (
                    battery_level, charging_state, charge_rate, energy_added, est_range, event_type
                ) VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                battery_level,
                charge['charging_state'],
                charge['charge_rate'],
                energy_added,
                charge['battery_range'],
                event_type
            ))

             # Prune oldest entries to keep max 30
            cur.execute("""
                DELETE FROM charge_log
                WHERE id NOT IN (
                    SELECT id FROM charge_log
                    ORDER BY timestamp DESC
                    LIMIT 30
                );
            """)
            
            conn.commit()
            print(f"✅ {event_type.upper()} session logged to database.")
