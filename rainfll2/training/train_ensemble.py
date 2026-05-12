# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import pandas as pd
# import numpy as np
# import joblib

# from xgboost import XGBRegressor
# from lightgbm import LGBMRegressor
# from sklearn.ensemble import RandomForestRegressor

# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score

# from features.feature_engineering import create_features

# # Load dataset
# df = pd.read_csv("data/india_rainfall_dataset.csv")

# # Feature engineering
# df = create_features(df)

# X = df.drop(["rain","date"],axis=1)
# y = df["rain"]

# print("Features:", X.columns)

# # Train test split
# X_train,X_test,y_train,y_test = train_test_split(
#     X,y,test_size=0.2,random_state=42
# )

# # Scaling
# scaler = StandardScaler()

# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

# # Models
# xgb = XGBRegressor(n_estimators=400,learning_rate=0.03,max_depth=7)

# lgb = LGBMRegressor(n_estimators=400,learning_rate=0.03,max_depth=7)

# rf = RandomForestRegressor(n_estimators=200,max_depth=10)

# # Train models
# xgb.fit(X_train,y_train)
# lgb.fit(X_train,y_train)
# rf.fit(X_train,y_train)

# # Predictions
# xgb_pred = xgb.predict(X_test)
# lgb_pred = lgb.predict(X_test)
# rf_pred = rf.predict(X_test)

# # Ensemble prediction
# final_pred = (
#     0.4*xgb_pred +
#     0.3*lgb_pred +
#     0.3*rf_pred
# )

# # Evaluate
# r2 = r2_score(y_test,final_pred)

# print("Ensemble R2 Score:", r2)

# # Save models
# joblib.dump(xgb,"models/xgb_model.pkl")
# joblib.dump(lgb,"models/lgb_model.pkl")
# joblib.dump(rf,"models/rf_model.pkl")
# joblib.dump(scaler,"models/scaler.pkl")

# print("Models saved successfully!")


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
import joblib

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from features.feature_engineering import create_features


# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/india_rainfall_dataset.csv")

df = create_features(df)

# -----------------------------
# Target transformation
# -----------------------------
df["rain_log"] = np.log1p(df["rain"])

X = df.drop(["rain","rain_log","date"], axis=1)
y = df["rain_log"]

print("Features used:", X.columns)

# -----------------------------
# Time-series split
# -----------------------------
split = int(len(X) * 0.8)

X_train = X[:split]
X_test = X[split:]

y_train = y[:split]
y_test = y[split:]


# -----------------------------
# Scaling
# -----------------------------
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# -----------------------------
# Models
# -----------------------------
xgb = XGBRegressor(
    n_estimators=400,
    max_depth=7,
    learning_rate=0.03,
    subsample=0.8,
    colsample_bytree=0.8
)

lgb = LGBMRegressor(
    n_estimators=400,
    max_depth=7,
    learning_rate=0.03,
    num_leaves=31,
    verbose=-1
)

rf = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    n_jobs=-1
)


# -----------------------------
# Train models
# -----------------------------
xgb.fit(X_train_scaled, y_train)
lgb.fit(X_train_scaled, y_train)
rf.fit(X_train_scaled, y_train)


# -----------------------------
# Predictions
# -----------------------------
xgb_pred = xgb.predict(X_test_scaled)
lgb_pred = lgb.predict(X_test_scaled)
rf_pred = rf.predict(X_test_scaled)


# -----------------------------
# Ensemble
# -----------------------------
y_pred = (
    0.4 * xgb_pred +
    0.3 * lgb_pred +
    0.3 * rf_pred
)


# -----------------------------
# Convert back from log
# -----------------------------
y_test_real = np.expm1(y_test)
y_pred_real = np.expm1(y_pred)


# -----------------------------
# Metrics
# -----------------------------
mae = mean_absolute_error(y_test_real, y_pred_real)
rmse = np.sqrt(mean_squared_error(y_test_real, y_pred_real))
r2 = r2_score(y_test_real, y_pred_real)

print("\nModel Performance")
print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)


# -----------------------------
# Save models
# -----------------------------
joblib.dump(xgb, "models/xgb_model.pkl")
joblib.dump(lgb, "models/lgb_model.pkl")
joblib.dump(rf, "models/rf_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

joblib.dump(X.columns.tolist(), "models/features.pkl")

print("\nAdvanced Ensemble Models Saved!")