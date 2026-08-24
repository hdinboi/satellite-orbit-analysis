import requests
from skyfield.api import EarthSatellite, load
from datetime import datetime, timedelta, UTC
from config import mu, earthRaidusKM, url

response = requests.get(url)

lines = response.text.strip().split('\n')


stationName = lines[0].strip()
line1 = lines[1]
line2 = lines[2]

ts = load.timescale()
satellite = EarthSatellite(line1, line2, stationName, ts)

daysAhead = int(input(f"How many days into the future do you want to predict the position of the {stationName}? "))

futureDate = datetime.now(UTC) + timedelta(days=daysAhead)

futureT = ts.utc(futureDate.year, futureDate.month, futureDate.day, futureDate.hour)

geocentric = satellite.at(futureT)
subpoint = geocentric.subpoint()

distFromCentre = geocentric.distance().km
altitude = distFromCentre - earthRaidusKM

print(f"Satellite: {stationName}")
print(f"Predicted position on {futureDate.strftime('%Y-%m-%d %H:%M')} UTC:")
print(f"Latitude: {subpoint.latitude.degrees:.4f}°")
print(f"Longitude: {subpoint.longitude.degrees:.4f}°")
print(f"Altitude: {altitude:.4f} km")