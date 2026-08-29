import requests
from skyfield.api import EarthSatellite, load
import csv
import os
from datetime import datetime
from config import url, earthRaidusKM, filename

#getting data for the ISS 


response = requests.get(url)

if response.status_code != 200 or "<!DOCTYPE" in response.text:
    print("Failed to get valid TLE data. Skipping this run.")
    exit()


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

distFromCentre = geocentric.distance().km
subpoint = geocentric.subpoint()

eccentricity = satellite.model.ecco
latitude = subpoint.latitude.degrees
longitude = subpoint.longitude.degrees
altitude = distFromCentre - earthRaidusKM

print(f"Satellite: {stationName}")
print(f"Latitude: :{latitude:.4f}°")
print(f"Longitude: {longitude:.4f}°")
print(f"Altitude: {altitude:.4f}km")

#save data to a CSV file

fileExists = os.path.exists(filename)

with open(filename, mode = 'a', newline='') as f:
    writer = csv.writer(f)
    
    #if file is new, write header
    if not fileExists:
        writer.writerow(["timestamp", "satellite", "latitude", "longitude", "altitude_km", "eccentricity"])
        
    writer.writerow([datetime.now(), stationName, latitude, longitude, altitude, eccentricity])

print(f"Data saved to {filename}")