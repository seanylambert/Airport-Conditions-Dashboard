# backend/database/db_connect.py

import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="historic_METAR",
        user="postgres",
        password="yourpassword"
    )
    print("✅ Connected to PostgreSQL!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)