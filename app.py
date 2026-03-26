import streamlit as st
import pandas as pd
from model import train_model, predict

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Vehicle Price Estimator", layout="centered")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
body {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

.stButton>button {
    background-color: #2563eb;
    color: white !important;
}

.stButton>button:hover {
    background-color: #1d4ed8;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA + MODEL
# =========================
@st.cache_resource
def load_all():
    df = pd.read_csv("data/sample_data.csv")
    df = df.dropna()

    model, X_test, _ = train_model()

    return df, model, X_test

# =========================
# LOADING UX (PLACEHOLDER)
# =========================
placeholder = st.empty()

with placeholder.container():
    st.markdown("### Initializing pricing engine...")
    st.caption("Loading model and preparing data...")
    st.progress(50)

df, model, X_test = load_all()

placeholder.empty()

# =========================
# TITLE
# =========================
st.markdown("## Vehicle Price Estimator")
st.caption("Real-time valuation for used vehicles based on market data")

st.divider()

# =========================
# INPUT
# =========================
st.subheader("Vehicle Details")

col1, col2 = st.columns(2)

with col1:
    year = st.slider("Year", 1990, 2023, 2015)
    odometer = st.number_input("Mileage (km)", 0, 300000, 50000)

with col2:
    manufacturer = st.selectbox("Manufacturer", sorted(df["manufacturer"].unique()))
    fuel = st.selectbox("Fuel Type", sorted(df["fuel"].unique()))

condition = st.selectbox("Condition", sorted(df["condition"].unique()))
transmission = st.selectbox("Transmission", sorted(df["transmission"].unique()))
vehicle_type = st.selectbox("Vehicle Type", sorted(df["type"].unique()))
paint_color = st.selectbox("Color", sorted(df["paint_color"].unique()))

# =========================
# ENCODING (CONSISTENTE CON MODELO)
# =========================
def encode(df, col, value):
    categories = df[col].astype("category").cat.categories
    mapping = dict(zip(categories, range(len(categories))))
    return mapping[value]

sample = X_test.iloc[0].copy()

sample["year"] = year
sample["odometer"] = odometer
sample["manufacturer"] = encode(df, "manufacturer", manufacturer)
sample["fuel"] = encode(df, "fuel", fuel)
sample["condition"] = encode(df, "condition", condition)
sample["transmission"] = encode(df, "transmission", transmission)
sample["type"] = encode(df, "type", vehicle_type)
sample["paint_color"] = encode(df, "paint_color", paint_color)

# =========================
# PREDICT
# =========================
if st.button("Calculate Vehicle Value"):

    result = predict(model, sample.to_dict())
    price = result["price"]

    st.markdown("---")
    st.markdown("### Valuation Result")

    st.metric("Estimated Price", f"${price:,.0f}")
    st.progress(min(price / 50000, 1.0))

    st.markdown("### Market Insight")

    if price < 5000:
        st.write("Low-value vehicle segment")
    elif price < 20000:
        st.write("Mid-range market vehicle")
    else:
        st.write("Premium segment vehicle")

    st.caption("Prediction powered by Machine Learning")