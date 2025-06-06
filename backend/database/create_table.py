# backend/database/create_table.py

import psycopg2

def create_table():
    try:
        conn = psycopg2.connect(
            dbname="historic_METAR",
            user="postgres",
            password="yourpassword",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS metar_reports (
                id SERIAL PRIMARY KEY,
                metar_id BIGINT,
                station_id VARCHAR(10),
                receipt_time TIMESTAMP,
                observation_time TIMESTAMP,
                report_time TIMESTAMP,
                temperature_c INTEGER,
                dewpoint_c INTEGER,
                wind_dir_degrees INTEGER,
                wind_speed_kt INTEGER,
                wind_gust_kt INTEGER,
                visibility_statute_mi VARCHAR(10),
                altimeter_hpa REAL,
                sea_level_pressure REAL,
                quality_control INTEGER,
                weather_string TEXT,
                pressure_tendency TEXT,
                max_temp INTEGER,
                min_temp INTEGER,
                max_temp_24hr INTEGER,
                min_temp_24hr INTEGER,
                precip REAL,
                precip_3hr REAL,
                precip_6hr REAL,
                precip_24hr REAL,
                snow_depth REAL,
                vertical_visibility INTEGER,
                metar_type VARCHAR(10),
                raw_text TEXT,
                most_recent BOOLEAN,
                latitude REAL,
                longitude REAL,
                elevation INTEGER,
                prior INTEGER,
                station_name TEXT,
                cloud_cover TEXT,
                cloud_base INTEGER
            );
        """)

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Error creating table:")
        print(e)


if __name__ == "__main__":
    create_table()