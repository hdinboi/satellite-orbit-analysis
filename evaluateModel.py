import pandas as pd
from config import filename
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

df = pd.read_csv(filename)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["altitude_km"] = pd.to_numeric(df["altitude_km"])

df = df.sort_values("timestamp")

df["altitude_smoothed"] = df["altitude_km"].rolling(window=5).mean()
df = df.dropna(subset=["altitude_smoothed"])

stationName = df["satellite"].iloc[0]


df["secondsElapsed"] = (df["timestamp"] - df["timestamp"].min()).dt.total_seconds()

#train/test split 80% train, 20% test

splitIndex = int(len(df)*0.8)
trainDf = df.iloc[:splitIndex]
testDf = df.iloc[splitIndex:]

model = LinearRegression()

model.fit(trainDf[["secondsElapsed"]], trainDf["altitude_smoothed"])

predictions = model.predict(testDf[["secondsElapsed"]])
actual = testDf["altitude_smoothed"]

#on average how many km off the models predictions were in the test period
MAE = mean_absolute_error(actual,predictions)

#same thing but weighted down more heavily toward big misses
RMSE = mean_squared_error(actual,predictions) ** 0.5

print(f"Tested on {len(testDf)} data points")
print(f"MAE: {MAE:.4f} km")
print(f"RMSE: {RMSE:.4f} km")
