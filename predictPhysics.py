import requests
from skyfield.api import EarthSatellite, load
from datetime import datetime, timedelta, UTC
from config import mu, earthRaidusKM, url


def fetchSatellite():
    response = requests.get(url)

    if response.status_code != 200 or "<!DOCTYPE" in response.text:
        raise ValueError("Failed to get valid TLE data from Celestrak.")

    lines = response.text.strip().split('\n')

    stationName = lines[0].strip()
    line1 = lines[1]
    line2 = lines[2]

    ts = load.timescale()
    satellite = EarthSatellite(line1, line2, stationName, ts)

    return satellite, stationName, ts


def predictPhysicsPosition(daysAhead):
    satellite, stationName, ts = fetchSatellite()

    futureDate = datetime.now(UTC) + timedelta(days=daysAhead)

    futureT = ts.utc(futureDate.year, futureDate.month, futureDate.day, futureDate.hour)

    geocentric = satellite.at(futureT)
    subpoint = geocentric.subpoint()

    distFromCentre = geocentric.distance().km
    altitude = distFromCentre - earthRaidusKM

    latitude = subpoint.latitude.degrees
    longitude = subpoint.longitude.degrees

    return stationName, futureDate, latitude, longitude, altitude


if __name__ == "__main__":
    daysAhead = int(input("How many days into the future do you want to predict the position of the ISS? "))

    stationName, futureDate, latitude, longitude, altitude = predictPhysicsPosition(daysAhead)

    print(f"Satellite: {stationName}")
    print(f"Predicted position on {futureDate.strftime('%Y-%m-%d %H:%M')} UTC:")
    print(f"Latitude: {latitude:.4f}°")
    print(f"Longitude: {longitude:.4f}°")
    print(f"Altitude: {altitude:.4f} km")