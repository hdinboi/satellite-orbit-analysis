import requests
from skyfield.api import EarthSatellite, load
import math
from datetime import datetime


#getting data for the ISS

url = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"
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
print(noKozai)
#noKozai is in radians per minute, we need revolutions per day of the satellite

meanMotion = (noKozai/ (2*(math.pi)) * 1440)
print(meanMotion)

#calculate observed period in minutes

T = 1440/meanMotion
print(f"Observed period: {T:.4f} minutes")

#calculate theoretical period
earthRaidusKM = 6371
mu = 398600.4418
t = ts.now()
geocentric = satellite.at(t)
subpoint = geocentric.subpoint()
altitide = subpoint.elevation.km

    #semi major axis approximation in km
a = earthRaidusKM + altitide

theoT = ((2*math.pi) * math.sqrt(a**3/mu))/60

print(f"Theoretical orbital period: {theoT:.4f} mintues")

#finding the percentage difference between the two
percentDiff = abs(T - theoT) / T*100
print(f"Difference: {percentDiff:.6f}%")




