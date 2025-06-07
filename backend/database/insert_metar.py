# python backend/database/insert_metar.py

import requests
import psycopg2
import time
import json
from datetime import datetime, timedelta, timezone

# Define your list of ICAO codes
ICAO_CODES = ['KRHV', 'KJFK', 'KSJC', 'KE16']  # User can edit this list

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'historic_METAR',
    'user': 'postgres',
    'password': 'yourpassword'
}

def fetch_metar(icao):
    url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]
    except Exception as e:
        print(f"Error fetching METAR for {icao}: {e}")
    return None

def obs_time_newer(cur, icao, obs_time):
    cur.execute("""
        SELECT observation_time FROM metar_reports
        WHERE station_id = %s
        ORDER BY observation_time DESC
        LIMIT 1;
    """, (icao,))
    row = cur.fetchone()
    if not row:
        return True  # no records yet

    last_obs_time = row[0]
    if last_obs_time.tzinfo is None:
        last_obs_time = last_obs_time.replace(tzinfo=timezone.utc)

    return obs_time > last_obs_time

def insert_metar(cur, data):
    cloud = data.get("clouds", [{}])[0]
    wdir_raw = data.get("wdir")
    if wdir_raw == "VRB":
        wdir = None
    else:
        try:
            wdir = int(wdir_raw) if wdir_raw is not None else None
        except ValueError:
            wdir = None

    metar_data = {
        "metar_id": data.get("metar_id"),
        "station_id": data.get("icaoId"),
        "receipt_time": data.get("receiptTime"),
        "observation_time": datetime.fromtimestamp(data.get("obsTime"), timezone.utc) if data.get("obsTime") else None,
        "report_time": data.get("reportTime"),
        "temp": data.get("temp"),
        "dewp": data.get("dewp"),
        "wdir": wdir,
        "wspd": data.get("wspd"),
        "wgst": data.get("wgst"),
        "visib": data.get("visib"),
        "altim": data.get("altim"),
        "slp": data.get("slp"),
        "qcField": data.get("qcField"),
        "wxString": data.get("wxString"),
        "presTend": data.get("presTend"),
        "maxT": data.get("maxT"),
        "minT": data.get("minT"),
        "maxT24": data.get("maxT24"),
        "minT24": data.get("minT24"),
        "precip": data.get("precip"),
        "pcp3hr": data.get("pcp3hr"),
        "pcp6hr": data.get("pcp6hr"),
        "pcp24hr": data.get("pcp24hr"),
        "snow": data.get("snow"),
        "vertVis": data.get("vertVis"),
        "metarType": data.get("metarType"),
        "rawOb": data.get("rawOb"),
        "mostRecent": bool(data.get("mostRecent")),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "elev": data.get("elev"),
        "prior": data.get("prior"),
        "name": data.get("name"),
        "cloud_cover": cloud.get("cover"),
        "cloud_base": cloud.get("base")
    }

    cur.execute("""
        INSERT INTO metar_reports (
            metar_id, station_id, receipt_time, observation_time, report_time,
            temperature_c, dewpoint_c, wind_dir_degrees, wind_speed_kt, wind_gust_kt,
            visibility_statute_mi, altimeter_hpa, sea_level_pressure, quality_control,
            weather_string, pressure_tendency, max_temp, min_temp, max_temp_24hr, min_temp_24hr,
            precip, precip_3hr, precip_6hr, precip_24hr, snow_depth, vertical_visibility,
            metar_type, raw_text, most_recent, latitude, longitude, elevation,
            prior, station_name, cloud_cover, cloud_base
        ) VALUES (
            %(metar_id)s, %(station_id)s, %(receipt_time)s, %(observation_time)s, %(report_time)s,
            %(temp)s, %(dewp)s, %(wdir)s, %(wspd)s, %(wgst)s,
            %(visib)s, %(altim)s, %(slp)s, %(qcField)s,
            %(wxString)s, %(presTend)s, %(maxT)s, %(minT)s, %(maxT24)s, %(minT24)s,
            %(precip)s, %(pcp3hr)s, %(pcp6hr)s, %(pcp24hr)s, %(snow)s, %(vertVis)s,
            %(metarType)s, %(rawOb)s, %(mostRecent)s, %(lat)s, %(lon)s, %(elev)s,
            %(prior)s, %(name)s, %(cloud_cover)s, %(cloud_base)s
        )
    """, metar_data)
    

def run():
    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            for icao in ICAO_CODES:
                metar = fetch_metar(icao)
                if metar and obs_time_newer(cur, icao, datetime.fromtimestamp(metar['obsTime'], tz=timezone.utc)):
                    # Clear old most_recent flags for this station
                    cur.execute("""
                        UPDATE metar_reports
                        SET most_recent = FALSE
                        WHERE station_id = %s AND most_recent = TRUE;
                    """, (icao,))

                    # Force mostRecent flag in metar_data to True, regardless of API
                    metar['mostRecent'] = True

                    insert_metar(cur, metar)
                    print(f"✅ Inserted METAR for {icao} at {metar['obsTime']}")
                else:
                    print(f"ℹ️ No new METAR for {icao}")

            conn.commit()
            cur.close()
            conn.close()

        except Exception as e:
            print("❌ Error during DB operation:", e)

        now = datetime.now(timezone.utc)
        next_fetch = now + timedelta(minutes=15)

        print(f"Last Fetch: {now.strftime('%Y-%m-%d %H:%M:%S %Z')} \nNext Fetch: {next_fetch.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        time.sleep(900)

if __name__ == "__main__":
    run()