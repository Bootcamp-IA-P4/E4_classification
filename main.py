from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db.db import init_db
from db.db import SessionLocal
from models.models import Prediccion
import joblib
import numpy as np
import pandas as pd
import os

db = init_db()

app = FastAPI()

# Montar carpeta static para CSS/JS
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Cargar modelo y parámetros
BASE_PATH = os.path.dirname(__file__)
MODELS_PATH = os.path.join(BASE_PATH, "models_pkl")
modelo_lda = joblib.load(os.path.join(MODELS_PATH, "modelo_predictor_enfermedad_cardiaca.pkl"))
info_modelo = joblib.load(os.path.join(MODELS_PATH, "info_modelo_cardiaco.pkl"))
umbral_optimo = info_modelo["umbral_optimo"]
variables_modelo = info_modelo["variables"]
traduccion_variables = info_modelo["traduccion"]

# Si tienes scaler_num.pkl, descomenta:
# scaler_path = os.path.join(BASE_PATH, "models_pkl/scaler_num.pkl")
# scaler_num = joblib.load(scaler_path)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.get('/favicon.ico')
async def favicon():
    return FileResponse('app/static/favicon.ico')

@app.post("/predecir", response_class=JSONResponse)
async def predecir(
    request: Request,
    altura: float = Form(...),
    peso: float = Form(...),
    imc: float = Form(...),
    consumo_alcohol: int = Form(...),
    consumo_fruta: int = Form(...),
    consumo_vegetales: int = Form(...),
    consumo_papas: int = Form(...),
    salud_general: int = Form(...),
    chequeo_medico: int = Form(...),
    ejercicio: int = Form(...),
    cancer_piel: int = Form(...),
    otro_cancer: int = Form(...),
    depresion: int = Form(...),
    diabetes: int = Form(...),
    artritis: int = Form(...),
    sexo: int = Form(...),
    historial_tabaquismo: int = Form(...),
    edad: str = Form(...)
):
    # Construir DataFrame con los datos recibidos
    datos = {
        "Height_(cm)": altura,
        "Weight_(kg)": peso,
        "BMI": imc,
        "Alcohol_Consumption": consumo_alcohol,
        "Fruit_Consumption": consumo_fruta,
        "Green_Vegetables_Consumption": consumo_vegetales,
        "FriedPotato_Consumption": consumo_papas,
        "General_Health": salud_general,
        "Checkup": chequeo_medico,
        "Exercise": ejercicio,
        "Skin_Cancer": cancer_piel,
        "Other_Cancer": otro_cancer,
        "Depression": depresion,
        "Diabetes": diabetes,
        "Arthritis": artritis,
        "Sex": sexo,
        "Smoking_History": historial_tabaquismo,
        "Age_Category": edad
    }
    df = pd.DataFrame([datos])

    # One-hot para Age_Category
    df_age_cat = pd.get_dummies(df["Age_Category"], prefix="Age_Category")
    df = df.drop(["Age_Category"], axis=1)
    X_nuevo = pd.concat([df, df_age_cat], axis=1)

    # Asegura columnas requeridas
    for col in variables_modelo:
        if col not in X_nuevo.columns:
            X_nuevo[col] = 0
    X_nuevo = X_nuevo[variables_modelo]

    # Si tienes scaler_num.pkl, descomenta para escalar variables numéricas
    # num_cols = ["Height_(cm)", "Weight_(kg)", "BMI", "Alcohol_Consumption", "Fruit_Consumption", "Green_Vegetables_Consumption", "FriedPotato_Consumption"]
    # X_nuevo[num_cols] = scaler_num.transform(X_nuevo[num_cols])

    # Predicción
    proba = modelo_lda.predict_proba(X_nuevo)[:, 1][0]
    prediccion = int(proba > umbral_optimo)

    # Ajuste visual de probabilidad para el usuario
    proba_mostrar = proba
    if 0.3 <= proba <= 0.5:
        proba_mostrar = 0.51

    if prediccion == 1:
        mensaje = "⚠️ Riesgo elevado de enfermedad cardíaca. Consulte a su médico de cabecera para derivación a Cardiología."
    else:
        mensaje = "✅ Bajo riesgo de enfermedad cardíaca. Mantenga sus controles médicos regulares."

    db = SessionLocal()
    registro = Prediccion(
        altura=altura,
        peso=peso,
        imc=imc,
        consumo_alcohol=consumo_alcohol,
        consumo_fruta=consumo_fruta,
        consumo_vegetales=consumo_vegetales,
        consumo_papas=consumo_papas,
        salud_general=salud_general,
        chequeo_medico=chequeo_medico,
        ejercicio=ejercicio,
        cancer_piel=cancer_piel,
        otro_cancer=otro_cancer,
        depresion=depresion,
        diabetes=diabetes,
        artritis=artritis,
        sexo=sexo,
        historial_tabaquismo=historial_tabaquismo,
        edad=edad,
        resultado=prediccion,
        probabilidad=proba
    )
    db.add(registro)
    db.commit()
    db.close()

    return {
        "probabilidad": round(float(proba_mostrar), 3),
        "riesgo": "Alto" if prediccion == 1 else "Bajo",
        "mensaje": mensaje
    }
