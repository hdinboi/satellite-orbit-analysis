import pandas as pd
import matplotlib.pyplot as plt

filename = "iss_data.csv"

df = pd.read_csv(filename)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["altitude_km"] = pd.to_numeric(df["altitude_km"])

plt.plot(df["timestamp"], df["altitude_km"])
plt.xlabel("Time")


plt.ylabel("Altitude (km)")
plt.xticks(rotation=45)
plt.title("ISS Altitude Over Time")
plt.tight_layout()
plt.show()
