# ==============================
# BASE IMAGE (estable y compatible)
# ==============================
FROM python:3.10-slim

# ==============================
# VARIABLES DE ENTORNO
# ==============================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ==============================
# WORKDIR
# ==============================
WORKDIR /app

# ==============================
# INSTALAR DEPENDENCIAS DEL SISTEMA
# ==============================
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# COPIAR REQUIREMENTS
# ==============================
COPY requirements.txt .

# ==============================
# INSTALAR DEPENDENCIAS PYTHON
# ==============================
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ==============================
# COPIAR PROYECTO
# ==============================
COPY . .

# ==============================
# EXPONER PUERTO STREAMLIT
# ==============================
EXPOSE 8501

# ==============================
# COMANDO DE EJECUCIÓN
# ==============================
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.fileWatcherType=none"]