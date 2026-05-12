

# import requests
# import datetime

# def get_nasa_weather(lat, lon):

#     url = "https://power.larc.nasa.gov/api/temporal/daily/point"

#     yesterday = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y%m%d")

#     params = {
#         "latitude": lat,
#         "longitude": lon,
#         "start": yesterday,
#         "end": yesterday,
#         "parameters": "PRECTOT,T2M,RH2M,PS",
#         "community": "AG",
#         "format": "JSON"
#     }

#     try:
#         res = requests.get(url, params=params)
#         data = res.json()

#         parameters = data.get("properties", {}).get("parameter", {})

#         precip = list(parameters.get("PRECTOT", {0:0}).values())[0]
#         temp = list(parameters.get("T2M", {0:0}).values())[0]
#         humidity = list(parameters.get("RH2M", {0:0}).values())[0]
#         pressure = list(parameters.get("PS", {0:0}).values())[0]

#         # NASA uses -999 for missing data
#         if temp == -999:
#             temp = 0
#         if humidity == -999:
#             humidity = 0
#         if pressure == -999:
#             pressure = 0

#     except Exception as e:

#         print("NASA API ERROR:", e)

#         precip = 0
#         temp = 0
#         humidity = 0
#         pressure = 0

#     return {
#         "sat_rain": precip,
#         "sat_temp": temp,
#         "sat_humidity": humidity,
#         "sat_pressure": pressure
#     }

import requests
import datetime

def get_nasa_weather(lat, lon):

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    date = (datetime.datetime.utcnow() - datetime.timedelta(days=3)).strftime("%Y%m%d")

    params = {
        "latitude": lat,
        "longitude": lon,
        "start": date,
        "end": date,
        "parameters": "PRECTOTCORR,T2M,RH2M,PS",  # ✅ FIXED
        "community": "AG",
        "format": "JSON"
    }

    try:
        res = requests.get(url, params=params)

        print("STATUS CODE:", res.status_code)

        data = res.json()
        parameters = data["properties"]["parameter"]

        precip = list(parameters["PRECTOTCORR"].values())[0]  # ✅ FIXED
        temp = list(parameters["T2M"].values())[0]
        humidity = list(parameters["RH2M"].values())[0]
        pressure = list(parameters["PS"].values())[0]

        def clean(val):
            return 0 if val in (-999, None) else val

        return {
            "sat_rain": clean(precip),
            "sat_temp": clean(temp),
            "sat_humidity": clean(humidity),
            "sat_pressure": clean(pressure)
        }

    except Exception as e:
        print("NASA API ERROR:", e)

        return {
            "sat_rain": 0,
            "sat_temp": 0,
            "sat_humidity": 0,
            "sat_pressure": 0
        }