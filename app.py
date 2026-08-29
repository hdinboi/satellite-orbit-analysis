import streamlit as st
import matplotlib.pyplot as plt
from predictData import loadModel, predictDataAltitude
from predictPhysics import predictPhysicsPosition
from evaluateModel import evaluateErrorModel
from orbitalAnalysis import orbitalPeriod

st.title("ISS Orbit Analysis and Prediction")

@st.cache_data(ttl=3600)
def getDataModel():
    return loadModel()

@st.cache_data(ttl=1800)
def getOrbitalPeriod():
    return orbitalPeriod()

@st.cache_data(ttl=1800)
def getPhysicsPrediction(daysAhead):
    return predictPhysicsPosition(daysAhead)

model, df, stationName = getDataModel()

st.write(f"Tracking : {stationName}")

st.subheader("Dataset Overview")
startDate = df["timestamp"].min()
endDate = df["timestamp"].max()
duration = endDate - startDate

MAE, RMSE, testSize = evaluateErrorModel()


overviewCol1, overviewCol2, overviewCol3 = st.columns(3)
overviewCol1.metric("Data points", len(df))
overviewCol2.metric("Time span", f"{duration.days}d {duration.seconds // 3600}h")
overviewCol3.metric("Latest reading", endDate.strftime('%Y-%m-%d %H:%M'))

st.subheader("Orbital Period: Observed vs Theoretical")
periodStation, meanMotion, observedPeriod, theoreticalPeriod, percentDiff = getOrbitalPeriod()

st.caption(f"{periodStation} orbits Earth {meanMotion:.2f} times every 24 hours")

col1, col2, col3 = st.columns(3)
col1.metric("Observed Period", f"{observedPeriod:.2f} min")
col2.metric("Theoretical (Kepler)", f"{theoreticalPeriod:.2f} min")
col3.metric("Difference", f"{percentDiff:.4f}%")

errorCol1, errorCol2 = st.columns(2)
errorCol1.metric("MAE", f"{MAE:.2f} km")
errorCol2.metric("RMSE", f"{RMSE:.2f} km")
st.caption(f"Evaluated on {testSize} held-out data points from historical data")

st.subheader("Altitude and Eccentricity Over Time")
fig, axes = plt.subplots(2, 1, figsize=(8, 8))

axes[0].plot(df["timestamp"], df["altitude_km"])
axes[0].set_xlabel("Time")
axes[0].set_ylabel("Altitude (km)")
axes[0].set_title(f"{stationName} Altitude Over Time")
axes[0].tick_params(axis='x', rotation=45)

axes[1].plot(df["timestamp"], df["eccentricity"])
axes[1].set_xlabel("Time")
axes[1].set_ylabel("Eccentricity")
axes[1].set_title(f"{stationName} Eccentricity Over Time")
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig)

st.subheader("Predict Future Altitude")
daysAhead = st.number_input("Days into the future:", min_value=1, max_value=30, value=3)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Physics-based (SGP4)")
    physicsStation, futureDate, latitude, longitude, physicsAltitude = getPhysicsPrediction(daysAhead)
    st.metric("Predicted Altitude", f"{physicsAltitude:.2f} km")
    st.caption(f"For {futureDate.strftime('%Y-%m-%d %H:%M')} UTC")
    st.caption(f"Lat: {latitude:.2f}°, Lon: {longitude:.2f}°")

with col2:
    st.markdown("### Data driven (Linear Regression)")
    dataFutureDate, dataAltitude = predictDataAltitude(model, df, daysAhead)
    st.metric("Predicted Altitude", f"{dataAltitude:.2f} km")
    st.caption(f"For {dataFutureDate.strftime('%Y-%m-%d %H:%M')} UTC")

st.info(
    "The physics model accounts for atmospheric drag however does not account for deliberate reboosts done to the satellite. "
    "The data based model can predict short term variances, but does not include orbital mechanics within its predictions. "
    "The difference between the two shows the individual blind spots of each approach."
)