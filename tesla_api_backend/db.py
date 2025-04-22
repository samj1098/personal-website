import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

#connection with PostgreSQL
def connect():
    return psycopg2.connect(DB_URL)