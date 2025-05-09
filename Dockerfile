# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente, modelos y recursos al contenedor
COPY . .

# Da permisos de lectura a los archivos .pkl
RUN chmod -R a+r /app/models_pkl

# Expone el puerto de la app Dash (8050)
EXPOSE 8050

# Comando por defecto para iniciar la app Dash
CMD ["python", "-m", "app.dashy"]
