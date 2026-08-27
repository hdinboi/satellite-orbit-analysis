import pandas as pd
from config import filename
from sklearn.linear_model import LinearRegression
from datetime import timedelta
#loading and preparing data
df = pd.read_csv(filename)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["altitude_km"] = pd.to_numeric(df["altitude_km"])

df = df.sort_values("timestamp")

df["altitude_smoothed"] = df["altitude_km"].rolling(window=5).mean()
df = df.dropna(subset=["altitude_smoothed"])

stationName = df["satellite"].iloc[0]


df["secondsElapsed"] = (df["timestamp"] - df["timestamp"].min()).dt.total_seconds()

#making prediction model using linear regression
model = LinearRegression()
model.fit(df[["secondsElapsed"]], df["altitude_smoothed"])

daysAhead = int(input(f"How many days into the future do you want to predict the position of {stationName}? "))

#date calcualtions
futureSeconds = df["secondsElapsed"].max() + (daysAhead * 24 * 60 * 60)
futureDate = df["timestamp"].min() + timedelta(seconds=futureSeconds)

futureDf = pd.DataFrame({"secondsElapsed": [futureSeconds]})
predictedAltitude = model.predict(futureDf)

print(f"Predicted date: {futureDate.strftime('%Y-%m-%d %H:%M')} UTC")
print(f"Predicted altitude in {daysAhead} days: {predictedAltitude[0]:.4f} km")