
import numpy as np
import pandas as pd
import joblib
import datetime
from tensorflow.keras.models import load_model
from api.nasa_api import get_nasa_weather


# -------------------------
# Load models
# -------------------------
xgb_model = joblib.load("models/xgb_model.pkl")
lgb_model = joblib.load("models/lgb_model.pkl")
rf_model = joblib.load("models/rf_model.pkl")
cat_model = joblib.load("models/cat_model.pkl")
scaler = joblib.load("models/scaler.pkl")
features = joblib.load("models/features.pkl")

lstm_model = load_model("models/lstm_model.h5", compile=False)


# -------------------------
# Spatial features
# -------------------------
def add_spatial_features(df, spatial_weather):

    if len(spatial_weather) == 0:
        df["neighbor_temp_avg"] = 0
        df["neighbor_humidity_avg"] = 0
        df["neighbor_pressure_avg"] = 0
        df["neighbor_cloud_avg"] = 0
        return df

    temps = [w["temp"] for w in spatial_weather]
    hums = [w["humidity"] for w in spatial_weather]
    press = [w["pressure"] for w in spatial_weather]
    clouds = [w["cloud"] for w in spatial_weather]

    df["neighbor_temp_avg"] = np.mean(temps)
    df["neighbor_humidity_avg"] = np.mean(hums)
    df["neighbor_pressure_avg"] = np.mean(press)
    df["neighbor_cloud_avg"] = np.mean(clouds)

    return df


# -------------------------
# Rain prediction
# -------------------------
def predict_rain(weather, history, spatial_weather):

    df = pd.DataFrame([weather])
  
    today = datetime.datetime.now()

    # NASA satellite weather
    sat = get_nasa_weather(weather["lat"], weather["lon"])
    print("NASA DATA:", sat)
    df["sat_rain"] = sat["sat_rain"]
    df["sat_temp"] = sat["sat_temp"]
    df["sat_humidity"] = sat["sat_humidity"]
    df["sat_pressure"] = sat["sat_pressure"]

    # Time features
    df["month"] = today.month
    df["day_of_year"] = today.timetuple().tm_yday

    # Rain history features
    df["rain_lag1"] = history[-1]
    df["rain_lag3"] = np.mean(history[-3:])
    df["rain_lag7"] = np.mean(history[-7:])

    df["rain_avg3"] = df["rain_lag3"]
    df["rain_avg7"] = df["rain_lag7"]

    # Interaction feature
    df["temp_humidity"] = df["temp"] * df["humidity"]

    # Season
    df["season"] = 1 if today.month in [6,7,8,9] else 0

    # Required features
    df["solar"] = 0
    df["rain_yes"] = 1 if history[-1] > 0 else 0

    # Spatial features
    # Spatial features
    df = add_spatial_features(df, spatial_weather)

# Ensure geographic features exist
    df["lat"] = weather["lat"]
    df["lon"] = weather["lon"]
    df["solar"] = 0

# Ensure dataframe contains all training features
    for col in features:
      if col not in df.columns:
        df[col] = 0

# Reorder columns exactly like training
    df = df[features]

# Scale
    X_scaled = scaler.transform(df)

    X = pd.DataFrame(X_scaled, columns=features)

    # ML predictions
    xgb_pred = xgb_model.predict(X)[0]
    lgb_pred = lgb_model.predict(X)[0]
    rf_pred = rf_model.predict(X)[0]
    cat_pred = cat_model.predict(X)[0]
    ml_pred = (
    0.35 * xgb_pred +
    0.30 * lgb_pred +
    0.20 * rf_pred +
    0.15 * cat_pred
)
    # LSTM prediction
    seq = np.array(history[-10:]).reshape(1, 10, 1)
    lstm_pred = lstm_model.predict(seq)[0][0]

    final = 0.7 * ml_pred + 0.3 * lstm_pred

    return max(final, 0)


# -------------------------
# 7 day forecast
# -------------------------
def predict_next_7_days(weather, history, spatial_weather):

    predictions = []

    temp_history = history.copy()

    for i in range(7):

        pred = predict_rain(weather, temp_history, spatial_weather)

        predictions.append(pred)

        temp_history.append(pred)

        temp_history = temp_history[-10:]

    return predictions