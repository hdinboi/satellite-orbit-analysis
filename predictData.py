import pandas as pd
from config import filename
from sklearn.linear_model import LinearRegression
from datetime import timedelta, UTC, datetime


def loadModel():
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

    return model, df, stationName



def predictDataAltitude(model, df, daysAhead):
    #date calcualtions
    targetDate = datetime.now(UTC) + timedelta(days=daysAhead)
    targetDate = targetDate.replace(tzinfo=None)
    futureSeconds = (targetDate - df["timestamp"].min()).total_seconds()
    

    futureDf = pd.DataFrame({"secondsElapsed": [futureSeconds]})
    predictedAltitude = model.predict(futureDf)

    return targetDate, predictedAltitude[0]



if __name__ == "__main__":
    model, df, stationName = loadModel()

    daysAhead = int(input(f"How many days into the future do you want to predict the position of {stationName}? "))

    futureDate, predictedAltitude = predictDataAltitude(model, df, daysAhead)

    print(f"Predicted date: {futureDate.strftime('%Y-%m-%d %H:%M')} UTC")
    print(f"Predicted altitude in {daysAhead} days: {predictedAltitude:.4f} km")