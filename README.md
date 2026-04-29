# Vehicle Price AI

Este proyecto lo desarrollé para analizar cómo diferentes variables influyen en el precio de vehículos usados y qué tan bien se pueden modelar con machine learning en un entorno real.

Incluye desde el análisis de datos hasta un modelo desplegado en producción con Streamlit.

 **Live Demo:** https://vehicle-price-ai.onrender.com  
 **Repository:** https://github.com/camargoluisenrique/vehicle-price-ai  

---

## Enfoque del proyecto

Más que solo entrenar un modelo, el objetivo fue construir un flujo completo:

- entender el dataset (EDA)
- identificar variables relevantes
- comparar modelos
- validar resultados
- desplegar una versión funcional accesible

El foco estuvo en balancear simplicidad, interpretabilidad y desempeño.
---

## Features

-  Price prediction in real time  
-  Model performance metrics (MAE, RMSE)  
-  Feature importance visualization  
-  Optimized dataset preview  
-  Public deployment (Render)  
-  USD → MXN conversion  

---

##  Model Performance

| Metric | Value |
|------|------|
| MAE | 3,549 |
| RMSE | 5,375 |

---

##  Application Preview

![Main App](images/app1.png)

![Prediction](images/app2.png)

![Feature Importance](images/app3.png)

![Dataset Preview](images/app4.png)

---

##  Machine Learning Pipeline

1. Data Cleaning (missing values, filtering)
2. Feature Engineering
3. Categorical Encoding (OneHotEncoder)
4. Model Training (Random Forest Regressor)
5. Evaluation (MAE, RMSE)
6. Deployment (Streamlit + Docker + Render)

---

##  Dataset

- Source: Kaggle (used vehicles dataset)
- Cleaned dataset: `clean_data.csv`
- Sample dataset: `sample_data.csv` (for lightweight UI preview)

---


## Resultado

Se obtuvo un modelo capaz de estimar precios con un error razonable para este tipo de dataset.

Más importante que la métrica final, este proyecto me permitió entender:

- qué variables realmente aportan valor
- cómo se comportan distintos modelos
- dónde aparecen problemas como overfitting

---

## Problemas encontrados

- Overfitting en modelos más complejos
- Variables categóricas con alta cardinalidad
- Ruido en el dataset

## Mejoras futuras

- Feature engineering más profundo
- Probar modelos como XGBoost o LightGBM
- Mejor validación del modelo

---

##  Tech Stack

- Python
- Pandas / NumPy
- Scikit-learn
- Streamlit
- Docker
- Render (deployment)

---

##  Run Locally

```bash
git clone https://github.com/camargoluisenrique/vehicle-price-ai.git
cd vehicle-price-ai

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

 Author

Luis Enrique Camargo    |   
Data Scientist | Applied Machine Learning
