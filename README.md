# 🚗 Vehicle Price Estimator (Machine Learning)

A production-style machine learning application that estimates the market value of used vehicles based on real-world data.

---

## 🚀 Live Demo

👉 (pega aquí tu link de Streamlit cuando deployes)

---

## 📊 Problem

Estimating the price of used vehicles is a complex regression problem due to:

- High variability in vehicle conditions
- Market-driven pricing dynamics
- Heterogeneous features (categorical + numerical)

This project simulates a real-world pricing engine similar to platforms like Kavak, Kelley Blue Book, or Carvana.

---

## ⚙️ Solution

Developed an end-to-end machine learning pipeline that:

- Cleans and filters noisy real-world data
- Encodes categorical variables efficiently
- Trains a regression model for price prediction
- Provides real-time predictions through a web application

---

## 🤖 Model

- Algorithm: Random Forest Regressor  
- Feature engineering + categorical encoding  
- Outlier filtering for price stability  

---

## 📈 Performance

- Mean Absolute Error (MAE): ~$3000  

This level of error is acceptable given the variability in used vehicle pricing.

---

## 💼 Business Perspective

The system enables:

- Fast vehicle valuation
- Price benchmarking for sellers
- Decision support for buyers and marketplaces

---

## 🧪 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

🧑‍💻 Author

Luis Enrique Camargo

Data Scientist | Machine Learning Engineer
