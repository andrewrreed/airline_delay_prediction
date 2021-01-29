# The following script loads the sampled dataset that was created in 3_data_processing.py (or loads
# the locally saved version if STORAGE_MODE=local) and trains an XGBoost classification model to predict
# if a flight will be cancelled based on a selected set of input features

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from joblib import dump, load
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

cancelled_flights = pd.read_csv("data/preprocessed_flight_data.csv")
cancelled_flights = cancelled_flights.dropna()

X = cancelled_flights[
    [
        "OP_CARRIER",
        "OP_CARRIER_FL_NUM",
        "ORIGIN",
        "DEST",
        "CRS_DEP_TIME",
        "CRS_ELAPSED_TIME",
        "DISTANCE",
        "WEEK",
        "HOUR",
    ]
]

y = cancelled_flights[["CANCELLED"]]

categorical_cols = ["OP_CARRIER", "OP_CARRIER_FL_NUM", "ORIGIN", "DEST"]
ct = ColumnTransformer(
    [("le", OneHotEncoder(), categorical_cols)], remainder="passthrough"
)

X_trans = ct.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_trans, y, random_state=42)

xgbclf = xgb.XGBClassifier()
pipe = Pipeline([("scaler", StandardScaler(with_mean=False)), ("xgbclf", xgbclf)])
pipe.fit(X_trans, y)

score = pipe.score(X_trans, y)
print("train", score)

os.mkdir("models/")
dump(pipe, "models/pipe.joblib")
dump(ct, "models/ct.joblib")