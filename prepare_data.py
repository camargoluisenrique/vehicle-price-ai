import pandas as pd

CHUNK_SIZE = 100_000

cols = [
    "price",
    "year",
    "manufacturer",
    "condition",
    "fuel",
    "odometer",
    "transmission",
    "type",
    "paint_color"
]

output_file = "data/clean_data.csv"

# borrar archivo si existe
open(output_file, "w").close()

first_chunk = True

print("🚀 Procesando dataset en chunks (modo PRO)...")

for chunk in pd.read_csv("data/vehicles_full.csv", chunksize=CHUNK_SIZE):

    chunk = chunk[cols].dropna()

    chunk = chunk[
        (chunk["price"] > 500) &
        (chunk["price"] < 100000) &
        (chunk["year"] > 1995) &
        (chunk["odometer"] < 300000)
    ]

    for col in ["manufacturer","condition","fuel","transmission","type","paint_color"]:
        chunk[col] = chunk[col].str.lower().str.strip()

    # escribir directamente a disco
    chunk.to_csv(output_file, mode="a", header=first_chunk, index=False)
    first_chunk = False

print("✅ clean_data.csv generado sin usar RAM excesiva")

# sample
df_sample = pd.read_csv(output_file).sample(n=300, random_state=42)
df_sample.to_csv("data/sample_data.csv", index=False)

print("🎯 sample_data.csv listo")