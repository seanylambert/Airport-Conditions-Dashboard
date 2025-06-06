# Flask server to fetch METAR data

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)
CORS(app)


@app.route("/metar")
def get_metar():
    station = request.args.get("station", "KRHV").upper()
    url = f"https://aviationweather.gov/api/data/metar?ids={station}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()  # ✅ Get Python list/dict first

        for report in data:
            obs_timestamp = report.get("obsTime")
            if obs_timestamp:
                try:
                    utc_time = datetime.fromtimestamp(obs_timestamp, tz=ZoneInfo("UTC"))
                    local_time = utc_time.astimezone(ZoneInfo("America/Los_Angeles"))
                    report["localObsTime"] = local_time.strftime("%Y-%m-%d %I:%M %p %Z")
                except Exception as e:
                    print("Error parsing obsTime:", obs_timestamp, e)
                    report["localObsTime"] = "Unknown"
            else:
                report["localObsTime"] = "Not provided"

        return jsonify(data)  # ✅ Now wrap the modified data

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)