#used for editing db
from db import connect

def add_event_type_column():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                ALTER TABLE charge_log
                ADD COLUMN IF NOT EXISTS event_type TEXT;
            """)
            conn.commit()
            print("✅ 'event_type' column added to charge_log.")

add_event_type_column()
