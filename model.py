import pandas as pd
import numpy as np
import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error

# =========================================
# PATHS
# =========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "clean_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# =========================================
# FEATURES
# =========================================
NUMERIC = ["year", "odometer"]

CATEGORICAL = [
    "manufacturer",
    "condition",
    "fuel",
    "transmission",
    "type",
    "paint_color"
]

FEATURES = NUMERIC + CATEGORICAL
TARGET = "price"

# =========================================
# LOAD DATA
# =========================================
def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES]
    y = df[TARGET]
    return X, y

# =========================================
# TRAIN MODEL
# =========================================
def train_and_save_model():
    X, y = load_data()

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", NUMERIC),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL)
        ]
    )

    model = Pipeline([
        ("preprocess", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=120,
            max_depth=12,
            random_state=42,
            n_jobs=-1
        ))
    ])

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    print("✅ Modelo entrenado y guardado en model.pkl")

    return model

# =========================================
# LOAD MODEL
# =========================================
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return train_and_save_model()

# =========================================
# PREP INPUT
# =========================================
def prepare_input(input_data):

    if isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
    else:
        df = pd.DataFrame([input_data])

    # mapping UI → modelo
    df = df.rename(columns={
        "mileage": "odometer",
        "fuel_type": "fuel"
    })

    # columnas faltantes
    for col in FEATURES:
        if col not in df.columns:
            if col in NUMERIC:
                df[col] = 0
            else:
                df[col] = "unknown"

    # orden correcto
    df = df[FEATURES]

    return df

# =========================================
# PREDICT
# =========================================
def predict_price(model, input_df):
    df = prepare_input(input_df)
    return model.predict(df)

# =========================================
# EVALUATION
# =========================================
def evaluate_model(model, X, y):
    preds = model.predict(X)
    mae = mean_absolute_error(y, preds)
    rmse = np.sqrt(mean_squared_error(y, preds))
    return mae, rmse

# =========================================
# FEATURE IMPORTANCE
# =========================================
def get_feature_importance(model):
    try:
        rf = model.named_steps["regressor"]
        preprocessor = model.named_steps["preprocess"]

        cat_features = preprocessor.named_transformers_["cat"].get_feature_names_out(CATEGORICAL)
        feature_names = list(NUMERIC) + list(cat_features)

        importances = rf.feature_importances_

        return pd.DataFrame({
            "feature": feature_names,
            "importance": importances
        }).sort_values(by="importance", ascending=False)

    except Exception as e:
        print("⚠️ Feature importance error:", e)
        return None

# =========================================
# RUN
# =========================================
if __name__ == "__main__":
    train_and_save_model()