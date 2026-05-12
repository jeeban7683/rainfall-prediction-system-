# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import pandas as pd
# import numpy as np
# import joblib
# from catboost import CatBoostRegressor
# from xgboost import XGBRegressor
# from lightgbm import LGBMRegressor
# from sklearn.ensemble import RandomForestRegressor

# from sklearn.model_selection import RandomizedSearchCV
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score

# from features.feature_engineering import create_features


# # Load data
# df = pd.read_csv("data/india_rainfall_dataset.csv")

# df = create_features(df)
# print("Dataset size:", len(df))
# print("First rows:")
# print(df.head())

# X = df.drop(["rain","date"],axis=1)
# y = df["rain"]
# print("Features used:")
# print(X.columns)

# print("Features:",X.columns)

# # Split
# from sklearn.model_selection import TimeSeriesSplit

# tscv = TimeSeriesSplit(n_splits=5)

# train_index, test_index = list(tscv.split(X))[-1]

# X_train, X_test = X.iloc[train_index], X.iloc[test_index]
# y_train, y_test = y.iloc[train_index], y.iloc[test_index]

# print("Train size:", len(X_train))
# print("Test size:", len(X_test))

# # Scale
# scaler = StandardScaler()

# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# X_train = pd.DataFrame(X_train_scaled, columns=X.columns)
# X_test = pd.DataFrame(X_test_scaled, columns=X.columns)

# # XGBoost Tuning

# xgb = XGBRegressor()
# xgb_params = {

#     "n_estimators":[300,500,800],
#     "max_depth":[6,8,10],
#     "learning_rate":[0.01,0.03],
#     "subsample":[0.7,0.8,0.9],
#     "colsample_bytree":[0.7,0.8,0.9]

# }


# xgb_search = RandomizedSearchCV(
#     xgb,
#     xgb_params,
#     n_iter=10,
#     cv=3,
#     scoring="r2",
#     n_jobs=-1
# )

# xgb_search.fit(X_train,y_train)

# xgb_best = xgb_search.best_estimator_

# print("Best XGBoost:",xgb_search.best_params_)


# # LightGBM Tuning

# lgb = LGBMRegressor()

# lgb_params = {

#     "n_estimators":[300,500,800],
#     "max_depth":[6,8,10],
#     "learning_rate":[0.01,0.03],
#     "num_leaves":[64,128,256],
#     "subsample":[0.7,0.8,0.9]

# }

# lgb_search = RandomizedSearchCV(
#     lgb,
#     lgb_params,
#     n_iter=10,
#     cv=3,
#     scoring="r2",
#     n_jobs=-1
# )

# lgb_search.fit(X_train,y_train)

# lgb_best = lgb_search.best_estimator_

# print("Best LightGBM:",lgb_search.best_params_)


# # RandomForest

# rf = RandomForestRegressor(
#     n_estimators=400,
#     max_depth=15,
#     min_samples_split=5,
#     n_jobs=-1
# )

# rf.fit(X_train,y_train)

# cat = CatBoostRegressor(
#     iterations=500,
#     depth=8,
#     learning_rate=0.03,
#     verbose=False
# )

# cat.fit(X_train,y_train)
# # Ensemble prediction

# xgb_pred = xgb_best.predict(X_test)
# lgb_pred = lgb_best.predict(X_test)
# rf_pred = rf.predict(X_test)
# cat_pred = cat.predict(X_test)
# final_pred = (

#     0.35 * xgb_pred +
#     0.30 * lgb_pred +
#     0.20 * rf_pred +
#     0.15 * cat_pred

# )

# r2 = r2_score(y_test,final_pred)

# print("Tuned Ensemble R2:",r2)



# # Save models

# joblib.dump(xgb_best,"models/xgb_model.pkl")
# joblib.dump(lgb_best,"models/lgb_model.pkl")
# joblib.dump(rf,"models/rf_model.pkl")
# joblib.dump(X.columns.tolist(),"models/features.pkl")
# joblib.dump(scaler,"models/scaler.pkl")
# joblib.dump(cat,"models/cat_model.pkl")
# print("Tuned models saved!")



import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
import joblib

from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
from sklearn.model_selection import TimeSeriesSplit

from features.feature_engineering import create_features


# -------------------------
# Load data
# -------------------------

df = pd.read_csv("data/india_rainfall_dataset.csv")

df = create_features(df)

print("Dataset size:", len(df))
print("First rows:")
print(df.head())


# -------------------------
# Features
# -------------------------

X = df.drop(["rain", "date"], axis=1)
y = df["rain"]

print("Features used:")
print(X.columns)


# -------------------------
# Remove infinity values
# -------------------------

X = X.replace([np.inf, -np.inf], np.nan)
X = X.dropna()

y = y.loc[X.index]


# -------------------------
# Time series split
# -------------------------

tscv = TimeSeriesSplit(n_splits=5)

train_index, test_index = list(tscv.split(X))[-1]

X_train, X_test = X.iloc[train_index], X.iloc[test_index]
y_train, y_test = y.iloc[train_index], y.iloc[test_index]

print("Train size:", len(X_train))
print("Test size:", len(X_test))


# -------------------------
# Scaling
# -------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train = pd.DataFrame(X_train_scaled, columns=X.columns)
X_test = pd.DataFrame(X_test_scaled, columns=X.columns)


# -------------------------
# XGBoost tuning
# -------------------------

xgb = XGBRegressor(tree_method="hist", random_state=42)

xgb_params = {

    "n_estimators": [200, 300, 500],
    "max_depth": [4, 6, 8],
    "learning_rate": [0.01, 0.03],
    "subsample": [0.7, 0.8, 0.9],
    "colsample_bytree": [0.7, 0.8, 0.9]

}

xgb_search = RandomizedSearchCV(
    xgb,
    xgb_params,
    n_iter=3,
    cv=2,
    scoring="r2",
    n_jobs=-1
)

xgb_search.fit(X_train, y_train)

xgb_best = xgb_search.best_estimator_

print("Best XGBoost:", xgb_search.best_params_)


# -------------------------
# LightGBM tuning
# -------------------------

lgb = LGBMRegressor(random_state=42)

lgb_params = {

    "n_estimators": [200, 300, 500],
    "max_depth": [4, 6, 8],
    "learning_rate": [0.01, 0.03],
    "num_leaves": [32, 64, 128],
    "subsample": [0.7, 0.8, 0.9]

}

lgb_search = RandomizedSearchCV(
    lgb,
    lgb_params,
    n_iter=3,
    cv=2,
    scoring="r2",
    n_jobs=-1
)

lgb_search.fit(X_train, y_train)

lgb_best = lgb_search.best_estimator_

print("Best LightGBM:", lgb_search.best_params_)


# -------------------------
# RandomForest
# -------------------------

rf = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    n_jobs=-1
)

rf.fit(X_train, y_train)


# -------------------------
# CatBoost
# -------------------------

cat = CatBoostRegressor(
    iterations=500,
    depth=6,
    learning_rate=0.03,
    loss_function="RMSE",
    verbose=False
)

cat.fit(X_train, y_train)


# -------------------------
# Predictions
# -------------------------

xgb_pred = xgb_best.predict(X_test)
lgb_pred = lgb_best.predict(X_test)
rf_pred = rf.predict(X_test)
cat_pred = cat.predict(X_test)


# -------------------------
# Ensemble
# -------------------------

final_pred = (

    0.35 * xgb_pred +
    0.30 * lgb_pred +
    0.20 * rf_pred +
    0.15 * cat_pred

)

r2 = r2_score(y_test, final_pred)

print("Tuned Ensemble R2:", r2)


# -------------------------
# Save models
# -------------------------

joblib.dump(xgb_best, "models/xgb_model.pkl")
joblib.dump(lgb_best, "models/lgb_model.pkl")
joblib.dump(rf, "models/rf_model.pkl")
joblib.dump(cat, "models/cat_model.pkl")

joblib.dump(X.columns.tolist(), "models/features.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("Tuned models saved!")