

import requests
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2
import datetime

API_KEY = "74a4ff9e64ae442ea8e150141260303"

# Load city coordinates dataset (must contain city, lat, lon)
cities_df = pd.read_csv("data/india_rainfall_dataset.csv")


# -------------------------------
# Get current weather
# -------------------------------
def get_weather_by_city(city):

    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

    res = requests.get(url)
    data = res.json()

    if "current" not in data:
        raise Exception(f"Weather API error: {data}")

    weather = {
        "temp": data["current"]["temp_c"],
        "humidity": data["current"]["humidity"],
        "pressure": data["current"]["pressure_mb"],
        "wind": data["current"]["wind_kph"],
        "cloud": data["current"]["cloud"],
        "lat": data["location"]["lat"],
        "lon": data["location"]["lon"]
    }

    return weather


# -------------------------------
# Get historical rainfall
# -------------------------------
def get_rain_history(city, days=14):

    history = []

    for i in range(days):

        date = (
            datetime.datetime.now()
            - datetime.timedelta(days=i + 1)
        ).strftime("%Y-%m-%d")

        url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={city}&dt={date}"

        res = requests.get(url)
        data = res.json()

        try:
            rain = data["forecast"]["forecastday"][0]["day"]["totalprecip_mm"]
        except:
            rain = 0

        history.append(rain)

    history.reverse()

    return history


# -------------------------------
# Haversine distance
# -------------------------------
def haversine(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat/2)**2 +
        cos(radians(lat1)) *
        cos(radians(lat2)) *
        sin(dlon/2)**2
    )

    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


# -------------------------------
# Find nearest cities
# -------------------------------
def find_nearest_cities(lat, lon, n=5):

    distances = []

    for _, row in cities_df.iterrows():

        dist = haversine(lat, lon, row["lat"], row["lon"])

        distances.append((row["lat"], row["lon"], dist))

    distances = sorted(distances, key=lambda x: x[2])

    nearest = [(lat, lon) for lat, lon, _ in distances[1:n+1]]

    return nearest

# -------------------------------
# Get spatial weather
# -------------------------------
def get_spatial_weather(main_city):

    main_weather = get_weather_by_city(main_city)

    lat = main_weather["lat"]
    lon = main_weather["lon"]

    nearest_locations = find_nearest_cities(lat, lon)

    spatial_weather = []

    for nlat, nlon in nearest_locations:

        try:

            url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={nlat},{nlon}"

            res = requests.get(url)
            data = res.json()

            w = {
                "temp": data["current"]["temp_c"],
                "humidity": data["current"]["humidity"],
                "pressure": data["current"]["pressure_mb"],
                "wind": data["current"]["wind_kph"],
                "cloud": data["current"]["cloud"]
            }

            spatial_weather.append(w)

        except:
            continue

    return spatial_weather