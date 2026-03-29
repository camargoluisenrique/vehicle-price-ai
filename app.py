import streamlit as st
import pandas as pd

from model import (
    load_model,
    predict_price,
    evaluate_model,
    get_feature_importance,
    load_data
)

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Vehicle Price AI", layout="centered")

# =========================
# CACHE
# =========================
@st.cache_resource
def load_model_cached():
    return load_model()

@st.cache_data
def load_sample_data():
    return pd.read_csv("data/sample_data.csv")

model = load_model_cached()
data = load_sample_data()

# =========================
# TITLE
# =========================
st.title("🚗 Vehicle Price AI")
st.write("Predict used vehicle prices using Machine Learning")

st.divider()

# =========================
# MODEL METRICS
# =========================
X, y = load_data()
mae, rmse = evaluate_model(model, X, y)

st.subheader("Model Performance")

col1, col2 = st.columns(2)
col1.metric("MAE", f"{mae:,.2f}")
col2.metric("RMSE", f"{rmse:,.2f}")

# =========================
# INPUTS
# =========================
st.subheader("Vehicle Features")

year = st.slider("Year", 2000, 2025, 2018)
mileage = st.number_input("Mileage (km)", value=50000)

manufacturer = st.selectbox("Manufacturer", ["ford","chevrolet","toyota","honda","bmw"])
condition = st.selectbox("Condition", ["like new","excellent","good","fair"])
fuel = st.selectbox("Fuel Type", ["gas","diesel","electric"])
transmission = st.selectbox("Transmission", ["automatic","manual"])
car_type = st.selectbox("Type", ["sedan","SUV","truck","coupe","van"])
paint_color = st.selectbox("Color", ["white","black","red","blue","silver"])

# =========================
# PREDICT
# =========================
if st.button("Predict Price"):

    input_data = pd.DataFrame({
        "year": [year],
        "odometer": [mileage],
        "manufacturer": [manufacturer],
        "condition": [condition],
        "fuel": [fuel],
        "transmission": [transmission],
        "type": [car_type],
        "paint_color": [paint_color]
    })

    prediction = predict_price(model, input_data)

    usd = prediction[0]
    mxn = usd * 17

    st.success(f"💰 Estimated Price: ${usd:,.2f} USD")
    st.info(f"🇲🇽 Precio estimado: ${mxn:,.2f} MXN")

# =========================
# FEATURE IMPORTANCE (FIX)
# =========================
importance_df = get_feature_importance(model)

if importance_df is not None:

    st.subheader("Feature Importance")

    top_features = importance_df.head(10)

    # tabla
    st.dataframe(top_features)

    # gráfica corregida (SIN ERROR)
    st.bar_chart(
        data=top_features,
        x="feature",
        y="importance"
    )

# =========================
# DATASET VIEW
# =========================
with st.expander("📂 View Sample Data"):

    st.write(f"Dataset size: {len(data)} rows")
    st.dataframe(data.head(20))