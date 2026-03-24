import streamlit as st
import pandas as pd
from model import train_model, predict

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Vehicle Price Estimator", layout="centered")

# =========================
# CUSTOM CSS
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
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 500;
    border: none;
}

.stButton>button:hover {
    background-color: #1d4ed8;
}

div[data-testid="stMetric"] {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL + DATA
# =========================
@st.cache_resource
def load_all():
    df = pd.read_csv("data/sample_data.csv")

    # limpiar (igual que modelo)
    df = df.dropna()

    mappings = {}
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("category")
        mappings[col] = dict(enumerate(df[col].cat.categories))
        df[col] = df[col].cat.codes

    model, X_test, _ = train_model()

    return model, X_test, mappings

# =========================
# LOADING UX
# =========================
placeholder = st.empty()

with placeholder.container():
    st.markdown("### Initializing pricing engine...")
    st.caption("Loading model and preparing data...")
    st.progress(50)

model, X_test, mappings = load_all()

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
    manufacturer = st.selectbox("Manufacturer", list(mappings["manufacturer"].values()))
    fuel = st.selectbox("Fuel Type", list(mappings["fuel"].values()))

condition = st.selectbox("Condition", list(mappings["condition"].values()))
transmission = st.selectbox("Transmission", list(mappings["transmission"].values()))
vehicle_type = st.selectbox("Vehicle Type", list(mappings["type"].values()))
paint_color = st.selectbox("Color", list(mappings["paint_color"].values()))

# =========================
# ENCODER
# =========================
def encode_value(col, value):
    reverse_map = {v: k for k, v in mappings[col].items()}
    return reverse_map[value]

# =========================
# SAMPLE INPUT
# =========================
sample = X_test.iloc[0].copy()

sample["year"] = year
sample["odometer"] = odometer
sample["manufacturer"] = encode_value("manufacturer", manufacturer)
sample["fuel"] = encode_value("fuel", fuel)
sample["condition"] = encode_value("condition", condition)
sample["transmission"] = encode_value("transmission", transmission)
sample["type"] = encode_value("type", vehicle_type)
sample["paint_color"] = encode_value("paint_color", paint_color)

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