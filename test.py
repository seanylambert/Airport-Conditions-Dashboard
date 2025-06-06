import requests

url = "https://aviationweather.gov/api/data/metar?ids=KRHV&format=json"
response = requests.get(url)
data = response.json()

print(data[0])  # First (and only) METAR