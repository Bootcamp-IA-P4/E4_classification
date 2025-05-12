# ❤️ HeartWise: Predicción de Riesgo Cardiovascular en la Era Digital

<div align="center">
    <img src="https://img.shields.io/badge/Cardio-Health-ff6f61?style=for-the-badge&logo=heartbeat&logoColor=white" alt="Cardio Health">
    <img src="https://img.shields.io/badge/Data-Prediction-4ECDC4?style=for-the-badge&logo=spark&logoColor=white" alt="Data Prediction">
</div>

> *Imagina un consultorio digital donde la ciencia de datos y la medicina preventiva se dan la mano para cuidar tu corazón.*

---

## 🎵 Bienvenido al Sistema Inteligente de Predicción de Riesgo Cardiaco 🎵

¡Descubre la aplicación más innovadora para predecir el riesgo de enfermedad cardíaca! Un proyecto que fusiona tecnología de vanguardia, ciencia de datos y experiencia clínica, transformando variables de salud en predicciones claras y útiles para la toma de decisiones.

---

## 🌊 La Historia Detrás del Proyecto 🌊

Todo comenzó cuando un equipo de entusiastas de la salud y la tecnología decidió llevar la predicción de riesgo cardiovascular a otro nivel:

1. **Análisis de Datos Profundo** 🔍: Exploramos exhaustivamente los datos clínicos, identificando patrones, correlaciones y variables clave. Documentamos cada paso en notebooks de EDA.
2. **Transformación Inteligente** 🔄: Convertimos variables categóricas a numéricas, estandarizamos valores y limpiamos outliers para obtener un dataset robusto.
3. **Batalla de Modelos** 🥊: Probamos varios algoritmos de clasificación, pero nos enfocamos en LDA (Análisis Discriminante Lineal) y Naive Bayes.
4. **LDA: El Modelo Elegido** 👑: Tras rigurosas pruebas, LDA se destacó por su capacidad de detectar la mayor cantidad de pacientes en riesgo (mayor recall), priorizando la prevención.

---

## 🎮 Características Innovadoras 🎮

* **Frontend Dash** 💾: Interfaz web interactiva y responsiva, 100% Python, sin JavaScript.
* **Predicción en Tiempo Real** 📊: Resultados inmediatos y visuales.
* **Flujo Paso a Paso** 🚶: Formulario guiado para capturar variables clínicas clave.
* **Persistencia en MySQL** 📜: Historial de predicciones seguro y consultable.
* **FastAPI + Docker** 💪: Backend rápido, seguro y portable.
* **Tests Automatizados** 🧪: Calidad garantizada en cada actualización.

---

## 📊 Variables del Modelo LDA 📊

Nuestro modelo utiliza un conjunto completo de variables clínicas para sus predicciones:

### Variables Numéricas y Categóricas:
- `height`: Altura (cm)
- `weight`: Peso (kg)
- `bmi`: Índice de masa corporal
- `general_health`: Salud general (1-5)
- `age_category`: Grupo de edad (ej: '30-40')
- `alcohol_consumption`: Consumo de alcohol (veces/semana)
- `fruit_consumption`: Consumo de frutas (veces/día)
- `green_vegetables_consumption`: Verduras verdes (veces/día)
- `fried_potato_consumption`: Papas fritas (veces/semana)
- `checkup`: Último chequeo médico (años)
- `exercise`: Ejercicio (días/semana)
- `skin_cancer`: Cáncer de piel (0=No, 1=Sí)
- `other_cancer`: Otros cánceres (0=No, 1=Sí)
- `depression`: Depresión (0=No, 1=Sí)
- `diabetes`: Diabetes (0=No, 1=Sí)
- `arthritis`: Artritis (0=No, 1=Sí)
- `sex`: Sexo biológico (0=M, 1=F)
- `smoking_history`: Historial tabaquismo (0=No, 1=Sí)

---

## 🔧 Pila Tecnológica 🔧

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Dash](https://img.shields.io/badge/Dash-2.x-00bfff?style=flat-square&logo=plotly)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green?style=flat-square&logo=fastapi)
![MySQL](https://img.shields.io/badge/MySQL-8.x-orange?style=flat-square&logo=mysql)
![Pandas](https://img.shields.io/badge/Pandas-1.5+-blueviolet?style=flat-square&logo=pandas)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.2+-orange?style=flat-square&logo=scikit-learn)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue?style=flat-square&logo=docker)
![pytest](https://img.shields.io/badge/pytest-8.3+-green?style=flat-square&logo=pytest)

---

## 📁 Estructura del Proyecto 📁

E4_classification/
├── backend/                          # Lógica de backend y API
│   ├── core/
│   │   └── config.py                 # Configuración principal del backend
│   ├── db/
│   │   ├── database.py               # Conexión y utilidades de base de datos
│   │   └── models.py                 # Modelos ORM (SQLAlchemy)
│   ├── create_back.py                # Script de inicialización backend
│   ├── dockerfile                    # Dockerfile para backend
│   └── ...                           # Otros módulos backend
│
├── client/                           # Frontend interactivo (Dash)
│   ├── __init__.py                   # Inicialización del módulo
│   ├── dashy.py                      # Aplicación Dash principal
│   ├── dashy_5.py                    # Variante de la app Dash
│   ├── dockerfile                    # Dockerfile para frontend
│   ├── assets/                       # Recursos estáticos (CSS, imágenes, etc.)
│   └── static/                       # Archivos JS estáticos
│
├── data/                             # Datos y modelos para ML
│   ├── CVD_cleaned.csv               # Dataset principal limpio
│
├── models/                           # Modelos y scripts auxiliares
│   └── models.py                     # Definición de modelos ML o utilidades
│
├── notebooks/                        # Notebooks de análisis y modelado
│   ├── models_notebooks/
│   │   ├── Datos_de_archivos.ipynb   # Análisis de archivos y variables
│   │   ├── EDA4.ipynb                # Exploración de datos avanzada
│   │   ├── EDA4_optuna.ipynb         # EDA con optimización de hiperparámetros
│   │   ├── MODELO_ELEGIDO.ipynb      # Notebook del modelo final elegido
│   │   └── ...                       # Otros notebooks de experimentación
│   └── models_pkl/
│       ├── info_modelo_cardiaco.pkl  # Info y metadatos del modelo
│       ├── main.py                   # Script de uso de modelos serializados
│       └── ...                       # Otros archivos PKL y scripts
│
├── test/                             # Pruebas automáticas
│   ├── __init__.py                   # Inicialización de tests
│   ├── conftest.py                   # Configuración de pytest
│   ├── test_model_integration.py     # Test de integración de modelo
│   └── tests.ipynb                   # Notebook de pruebas
│
├── venv/                             # Entorno virtual (ignorado por git)
│
├── compose.yaml                      # Orquestación de servicios Docker
├── requirements.txt                  # Dependencias del proyecto
├── .env                              # Variables de entorno
├── .env.example                      # Ejemplo de configuración de entorno
├── .gitignore                        # Archivos y carpetas ignorados por git
├── .dockerignore                     # Archivos ignorados por Docker
├── README.md                         # Documentación principal
└── README2.md                        # Documentación alternativa/histórica

---

## 🚦 Flujo de la Aplicación

1. **El usuario** ingresa sus datos clínicos en la interfaz Dash.
2. **Dash** envía los datos al backend FastAPI vía HTTP (JSON).
3. **FastAPI** procesa los datos, ejecuta el modelo LDA y almacena la predicción en MySQL.
4. **El resultado** (nivel de riesgo y probabilidad) se muestra automáticamente en la interfaz, junto con visualizaciones y mensajes interpretativos.

---

## 🧠 Proceso de Ciencia de Datos

### 1. EDA y Selección de Modelo

- Analizamos y limpiamos los datos, identificando valores atípicos y desbalance de clases.
- Balanceamos el dataset con submuestreo y SMOTE.
- Probamos varios modelos, eligiendo LDA por su alto recall (mejor para no dejar enfermos sin detectar).

### 2. Retos y Decisiones

- **Desbalance:** Muchos más sanos que enfermos, lo que dificulta la detección de casos positivos.
- **Comparación de modelos:** Elegimos LDA porque en salud es mejor advertir de más que dejar pasar un enfermo sin tratar.

#### Ejemplo Didáctico

> Imagina una red para atrapar peces enfermos:
> - Red NaiveBayes: Atrapa pocos enfermos pero casi nunca se equivoca (alta precisión, bajo recall).
> - Red LDA: Atrapa más enfermos, aunque a veces atrapa sanos por error (alto recall, menor precisión).
> - **En salud, preferimos LDA para no dejar enfermos sin detectar.**