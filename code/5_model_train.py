# ###########################################################################
#
#  CLOUDERA APPLIED MACHINE LEARNING PROTOTYPE (AMP)
#  (C) Cloudera, Inc. 2021
#  All rights reserved.
#
#  Applicable Open Source License: Apache 2.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
# ###########################################################################

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

categorical_cols = ["OP_CARRIER", "ORIGIN", "DEST"]
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
