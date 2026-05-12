import streamlit as st
from api.weather_api import get_weather_by_city, get_rain_history, get_spatial_weather
from prediction.predict import predict_rain, predict_next_7_days
import matplotlib.pyplot as plt

st.title("🌧️ AI Rainfall Prediction System")

city = st.text_input("Enter City Name")

if st.button("Predict Rainfall"):

    with st.spinner("Analyzing weather patterns..."):
     weather = get_weather_by_city(city)
    spatial_weather = get_spatial_weather(city)

    history = get_rain_history(city)

    # Today's prediction
    today_rain = predict_rain(weather, history, spatial_weather)

    st.subheader("📍 Location")
    st.write(city)

    if today_rain > 2:
        st.success(f"🌧 Rain Expected Today: {round(today_rain,2)} mm")
    else:
        st.info("☀ No Rain Expected Today")

    # 7 day forecast
    forecast = predict_next_7_days(weather, history, spatial_weather)

    st.subheader("📅 7 Day Rainfall Forecast")

    for i, rain in enumerate(forecast):

        if rain > 2:
            st.write(f"Day {i+1}: 🌧️ {round(rain,2)} mm")
        else:
            st.write(f"Day {i+1}: 🌤️ No Rain")

    # Graph
    fig, ax = plt.subplots()

    ax.plot(range(1,8), forecast, marker="o")

    ax.set_xlabel("Day")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_title("7 Day Rainfall Forecast")

    st.pyplot(fig)