import pandas as pd

# =========================
# LOAD DATASET ORIGINAL
# =========================
df = pd.read_csv("data/vehicles.csv")

# =========================
# LIMPIEZA (MISMA LÓGICA QUE MODELO)
# =========================
df = df.drop(columns=[
    'id','url','region','region_url','VIN','image_url',
    'description','county','state','lat','long','posting_date'
], errors="ignore")

df = df.dropna(subset=[
    'price','year','manufacturer','condition','fuel',
    'odometer','transmission','type','paint_color'
])

# filtro de precios realistas
df = df[(df["price"] > 500) & (df["price"] < 100000)]

# eliminar columna problemática
df = df.drop(columns=["model"], errors="ignore")

# =========================
# SAMPLE (200 FILAS)
# =========================
df_small = df.sample(n=200, random_state=42)

# limpieza final (por seguridad)
df_small = df_small.dropna()

# =========================
# GUARDAR
# =========================
df_small.to_csv("data/sample_data.csv", index=False)

print("✅ sample_data.csv generado con 200 filas limpias")