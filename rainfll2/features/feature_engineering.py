import pandas as pd
import numpy as np

def create_features(df):

    df["date"] = pd.to_datetime(df["date"])

    # Time features
    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear

    # Cyclical encoding
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    df["day_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
    df["day_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365)

    # Lag rainfall
    df["rain_lag1"] = df["rain"].shift(1)
    df["rain_lag3"] = df["rain"].shift(3)
    df["rain_lag7"] = df["rain"].shift(7)
    df["rain_lag14"] = df["rain"].shift(14)
    df["rain_lag30"] = df["rain"].shift(30)

    # Rolling rainfall
    df["rain_sum7"] = df["rain"].rolling(7).sum()
    df["rain_sum14"] = df["rain"].rolling(14).sum()
    df["rain_sum30"] = df["rain"].rolling(30).sum()

    df["rain_avg7"] = df["rain"].rolling(7).mean()
    df["rain_std7"] = df["rain"].rolling(7).std()

    # Weather interaction
    df["temp_humidity"] = df["temp"] * df["humidity"]
    df["humidity_temp_ratio"] = df["humidity"] / (df["temp"] + 1)

    # Weather changes
    df["humidity_change"] = df["humidity"].diff()
    df["pressure_change"] = df["pressure"].diff()

    # Seasonal flags
    df["is_monsoon"] = df["month"].isin([6,7,8,9]).astype(int)
    df["is_winter"] = df["month"].isin([12,1,2]).astype(int)

    df["rain_yes"] = (df["rain"] > 0).astype(int)
    df = df.dropna()

    return df