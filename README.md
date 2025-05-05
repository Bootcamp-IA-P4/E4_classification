# Guía de Inicio Rápido

---

## 🚀 Pasos para ejecutar la aplicación Dash y conectar con la base de datos

### 1. Clona el repositorio y navega a la carpeta del proyecto

```bash
cd E4_classification
```

### 2. Instala las dependencias necesarias

Asegúrate de tener Python 3.8+ instalado. Luego ejecuta:

```bash
pip install -r requirements.txt
```

### 3. Configura la base de datos

- Crea una base de datos MySQL con los parámetros indicados en el archivo `.env` (puedes modificar los valores según tu entorno):
  - MYSQL_USER
  - MYSQL_PASSWORD
  - MYSQL_HOST
  - MYSQL_PORT
  - MYSQL_DB

- Asegúrate de que el usuario y la contraseña tengan permisos para crear tablas y escribir datos.

### 4. Verifica la configuración del archivo `.env`

El archivo `.env` debe estar en la raíz del proyecto y contener los datos de conexión a la base de datos. Ejemplo:

```
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=registros_usuarios
```

### 5. Ejecuta la aplicación Dash

Desde la raíz del proyecto, ejecuta:

```bash
python -m app.dashy
```

Esto iniciará la aplicación Dash. Por defecto, estará disponible en [http://127.0.0.1:8050](http://127.0.0.1:8050)

### 6. Uso de la aplicación

- Ingresa los datos requeridos en la interfaz web.
- Al enviar el formulario, la predicción se almacenará automáticamente en la base de datos configurada.

---

# Proyecto de Clasificación

---

## 📝 Descripción del Proyecto

Este proyecto consiste en desarrollar un modelo de machine learning para resolver un problema de **clasificación**. El objetivo es crear una solución capaz de predecir una clase (por ejemplo, la satisfacción de clientes) a partir de ciertos parámetros, utilizando un dataset adecuado (sugerido: Airlines Dataset, aunque se recomienda buscar uno propio para mayor autenticidad).

La solución final debe incluir una aplicación que reciba los datos de un cliente y devuelva la predicción de clasificación, además de un informe técnico y una presentación para negocio.

---

## 📦 Condiciones de Entrega

- Proyecto grupal.
- Entregar:
  - Aplicación funcional (Streamlit, Gradio, Dash, etc.) que reciba datos y devuelva la predicción.
  - Repositorio en GitHub con ramas ordenadas y mensajes de commit claros.
  - Informe técnico del rendimiento del modelo (métricas y explicación).
  - Presentación para negocio y presentación técnica del código.
  - Enlace a Trello u otra herramienta de organización.
  - Overfitting inferior al 5%.

---

## 🛠️ Tecnologías a Usar

- Scikit-learn
- Pandas
- Streamlit / Dash / Gradio
- Git y GitHub
- Docker

---

## 🏆 Niveles de Entrega

### 🟢 Nivel Esencial

- Modelo de clasificación funcional.
- Análisis exploratorio de datos (EDA) con visualizaciones relevantes.
- Overfitting < 5%.
- Solución productivizada (app web/API).
- Informe de métricas de clasificación (accuracy, recall, precision, F1, ROC, matriz de confusión, etc.) y explicación del performance.

### 🟡 Nivel Medio

- Modelos ensemble (Random Forest, Gradient Boosting, XGBoost, etc.).
- Validación cruzada (K-Fold, Leave-One-Out).
- Optimización de hiperparámetros (GridSearch, RandomSearch, Optuna, etc.).
- Sistema de feedback y monitorización en producción.
- Pipeline de ingestión de nuevos datos.

### 🟠 Nivel Avanzado

- Dockerización del programa.
- Guardado de datos en bases de datos (SQL, MongoDB, etc.).
- Despliegue en la nube (AWS, GCP, Azure, Render, Vercel, etc.).
- Test unitarios (validación de preprocesamiento, métricas mínimas, etc.).

### 🔴 Nivel Experto

- Experimentos/despliegues con redes neuronales.
- MLOps: A/B Testing, monitoreo de data drift, auto-reemplazo de modelos.

---

## 🎯 Evaluación

- Evaluar datasets con herramientas de análisis y visualización.
- Aplicar algoritmos de ML según el problema, identificando y resolviendo problemas clásicos de IA.

---

## Estructura Inicial del Proyecto

- Este repositorio contiene la estructura base y archivos vacíos para comenzar el desarrollo. A medida que avances, agrega notebooks, scripts, documentación y recursos en las carpetas correspondientes.