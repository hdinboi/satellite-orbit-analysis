import pandas as pd
import matplotlib.pyplot as plt

filename = "iss_data.csv"
#creating dataframe to read columns from the CSV file
df = pd.read_csv(filename)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["altitude_km"] = pd.to_numeric(df["altitude_km"])
df["eccentricity"] = pd.to_numeric(df["eccentricity"])
#making one window to fit both graphs
fig, axes = plt.subplots(2, 1, figsize=(8, 8))
#altitude over time
axes[0].plot(df["timestamp"], df["altitude_km"])
axes[0].set_xlabel("Time")
axes[0].set_ylabel("Altitude (km)")
axes[0].set_title("ISS Altitude Over Time")
axes[0].tick_params(axis='x', rotation=45)
#eccentricity over time
axes[1].plot(df["timestamp"], df["eccentricity"])
axes[1].set_xlabel("Time")
axes[1].set_ylabel("Eccentricity")
axes[1].set_title("ISS Eccentricity Over Time")
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()