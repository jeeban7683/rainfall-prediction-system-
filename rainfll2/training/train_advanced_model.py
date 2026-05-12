

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from catboost import CatBoostRegressor

from features.feature_engineering import create_advanced_features, create_features


# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("data/india_rainfall_dataset.csv")

print("Dataset size:", len(df))

# -------------------------
# Feature engineering
# -------------------------
df = create_advanced_features(df)

# Log transform rain
df["rain"] = np.log1p(df["rain"])

# -------------------------
# Features
# -------------------------
features = [c for c in df.columns if c not in ["rain", "date"]]

print("Features used:", features)

X = df[features]
y = df["rain"]

# -------------------------
# Train test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# Scaling
# -------------------------
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------
# Models
# -------------------------

xgb_model = XGBRegressor(
    n_estimators=1500,
    max_depth=10,
    learning_rate=0.02,
    subsample=0.8,
    colsample_bytree=0.8,
    tree_method="hist"
)

lgb_model = LGBMRegressor(
    n_estimators=2000,
    learning_rate=0.02,
    num_leaves=128,
    max_depth=12
)

rf_model = RandomForestRegressor(
    n_estimators=500,
    max_depth=20,
    n_jobs=-1
)

cat_model = CatBoostRegressor(
    iterations=1500,
    depth=10,
    learning_rate=0.03,
    verbose=False
)

# -------------------------
# Train models
# -------------------------
xgb_model.fit(X_train_scaled, y_train)
lgb_model.fit(X_train_scaled, y_train)
rf_model.fit(X_train_scaled, y_train)
cat_model.fit(X_train_scaled, y_train)

# -------------------------
# Predictions
# -------------------------
xgb_pred = xgb_model.predict(X_test_scaled)
lgb_pred = lgb_model.predict(X_test_scaled)
rf_pred = rf_model.predict(X_test_scaled)
cat_pred = cat_model.predict(X_test_scaled)

# Ensemble
final_pred = (
    0.35 * xgb_pred +
    0.30 * lgb_pred +
    0.20 * rf_pred +
    0.15 * cat_pred
)

# -------------------------
# Evaluation
# -------------------------
score = r2_score(y_test, final_pred)

print("Advanced Ensemble R2:", score)

# -------------------------
# Save models
# -------------------------
joblib.dump(xgb_model, "models/xgb_model.pkl")
joblib.dump(lgb_model, "models/lgb_model.pkl")
joblib.dump(rf_model, "models/rf_model.pkl")
joblib.dump(cat_model, "models/cat_model.pkl")

joblib.dump(scaler, "models/scaler.pkl")
joblib.dump(features, "models/features.pkl")

print("Models saved successfully!")