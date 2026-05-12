import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import joblib
import numpy as np

from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from features.feature_engineering import create_features

# Load data
df = pd.read_csv('data/india_rainfall_dataset.csv')

# Feature engineering
df = create_features(df)

X = df.drop(['rain','date'], axis=1)
y = df['rain']

print("Features used:", X.columns)

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Time-series split (better for weather data)
tscv = TimeSeriesSplit(n_splits=5)

model = XGBRegressor(
    n_estimators=400,
    learning_rate=0.03,
    max_depth=7,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1,
    random_state=42
)

mae_scores = []
rmse_scores = []
r2_scores = []

for train_idx, test_idx in tscv.split(X_scaled):

    X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae_scores.append(mean_absolute_error(y_test, y_pred))
    rmse_scores.append(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2_scores.append(r2_score(y_test, y_pred))


print("\nAverage Performance")

print("MAE:", np.mean(mae_scores))
print("RMSE:", np.mean(rmse_scores))
print("R2 Score:", np.mean(r2_scores))

# Train final model on all data
model.fit(X_scaled, y)

# Save model
joblib.dump(model, 'models/xgb_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

print("\nModel saved successfully")

