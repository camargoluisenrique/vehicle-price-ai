from pyngrok import ngrok
import os

# abrir túnel en puerto 8501 (streamlit)
public_url = ngrok.connect(8501)

print("\n==============================")
print("🚀 TU APP ESTÁ EN ESTE LINK:")
print(public_url)
print("==============================\n")

# ejecutar streamlit
os.system("streamlit run app.py")