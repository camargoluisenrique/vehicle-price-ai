import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# =========================
# LOAD & CLEAN DATA
# =========================
def load_data():
    df = pd.read_csv("data/vehicles.csv")

    # eliminar columnas basura
    df = df.drop(columns=[
        'id','url','region','region_url','VIN','image_url',
        'description','county','state','lat','long','posting_date'
    ], errors="ignore")

    # eliminar nulos importantes
    df = df.dropna(subset=[
        'price','year','manufacturer','condition','fuel',
        'odometer','transmission','type','paint_color'
    ])

    # filtrar precios irreales
    df = df[(df["price"] > 500) & (df["price"] < 100000)]

    # eliminar modelo (alta cardinalidad)
    df = df.drop(columns=["model"], errors="ignore")

    # encoding categórico
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("category").cat.codes

    X = df.drop("price", axis=1)
    y = df["price"]

    return X, y


# =========================
# TRAIN MODEL
# =========================
def train_model():
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    print(f"🔥 MAE: {mae:.2f}")

    return model, X_test, y_test


# =========================
# PREDICT
# =========================
def predict(model, input_data):
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]

    return {
        "price": float(prediction)
    }

# =========================
# RUN
# =========================
if __name__ == "__main__":
    model, X_test, y_test = train_model()