import requests
from skyfield.api import EarthSatellite, load
import math
from datetime import datetime
from config import mu, earthRaidusKM, url


def orbitalPeriod():
    #getting data for the ISS

    response = requests.get(url)

    lines = response.text.strip().split('\n')

    #split data into 3 seperate lines

    stationName = lines[0].strip()
    line1 = lines[1]
    line2 = lines[2]

    ts = load.timescale()
    satellite = EarthSatellite(line1, line2, stationName, ts)

    #getting mean motion of ISS

    noKozai = satellite.model.no_kozai

    #noKozai is in radians per minute, we need revolutions per day of the satellite

    meanMotion = (noKozai/ (2*(math.pi)) * 1440)

    #calculate observed period in minutes

    T = 1440/meanMotion

    #calculate theoretical period
    t = ts.now()
    geocentric = satellite.at(t)
    distFromCentre = geocentric.distance().km
    subpoint = geocentric.subpoint()
    altitide = distFromCentre - earthRaidusKM

        #semi major axis approximation in km
    a = earthRaidusKM + altitide

    theoT = ((2*math.pi) * math.sqrt(a**3/mu))/60

    #finding the percentage difference between the two
    percentDiff = (abs(T - theoT) / T)*100

    return stationName, meanMotion, T, theoT, percentDiff


if __name__ == "__main__":
    stationName, meanMotion, T, theoT, percentDiff = orbitalPeriod()

    print(f"{stationName} orbits Earth {meanMotion:.4f} times in 24 hours.")
    print(f"Observed period: {T:.4f} minutes")
    print(f"Theoretical orbital period: {theoT:.4f} mintues")
    print(f"Difference: {percentDiff:.6f}%")