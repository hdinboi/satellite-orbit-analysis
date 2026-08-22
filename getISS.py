import requests
from skyfield.api import EarthSatellite, load
import csv
import os
from datetime import datetime


#getting data for the ISS

url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"
response = requests.get(url)
print(response.status_code)
print(response.text[:200])

lines = response.text.strip().split('\n')

#split data into 3 seperate lines

stationName = lines[0].strip()
line1 = lines[1]
line2 = lines[2]

ts = load.timescale()
satellite = EarthSatellite(line1, line2, stationName, ts)

#getting current position of ISS
t = ts.now()
    #where is satellite in relation to centre of earth at this exact time
geocentric = satellite.at(t)
subpoint = geocentric.subpoint()

latitude = subpoint.latitude.degrees
longitude = subpoint.longitude.degrees
altitude = subpoint.elevation.km

print(f"Satellite: {stationName}")
print(f"Latitude: :{latitude:.4f}°")
print(f"Longitude: {longitude:.4f}°")
print(f"Altitude: {altitude:.4f}km")

#save data to a CSV file for later analysis and prediction
filename = "iss_data.csv"
fileExists = os.path.exists(filename)

with open(filename, mode = 'a', newline='') as f:
    writer = csv.writer(f)
    
    #if file is new, write header
    if not fileExists:
        writer.writerow(["timestamp", "satellite", "latitude", "longitude", "altitude_km"])
        
    writer.writerow([datetime.now(), stationName, latitude, longitude, altitude])

print(f"Data saved to {filename}")