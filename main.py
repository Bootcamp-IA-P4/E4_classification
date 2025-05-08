from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response
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

# Diccionarios de traducción
sexo_dict = {0: "Masculino", 1: "Femenino"}
artritis_dict = {0: "No", 1: "Sí"}
diabetes_dict = {
    0: "No",
    1: "No, pre-diabetes o borderline",
    2: "Sí",
    3: "Sí, solo durante embarazo"
}
depresion_dict = {0: "No", 1: "Sí"}
cancer_piel_dict = {0: "No", 1: "Sí"}
otro_cancer_dict = {0: "No", 1: "Sí"}
ejercicio_dict = {0: "No", 1: "Sí"}
historial_tabaquismo_dict = {0: "No", 1: "Sí"}
salud_general_dict = {
    0: "Mala",
    1: "Regular",
    2: "Buena",
    3: "Muy buena",
    4: "Excelente"
}
chequeo_medico_dict = {
    0: "Nunca",
    1: "Hace 5 años o más",
    2: "En los últimos 5 años",
    3: "En los últimos 2 años",
    4: "En el último año"
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.get('/favicon.ico')
async def favicon():
    favicon_path = 'app/static/favicon.ico'
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    # Devuelve un 204 No Content si no existe el favicon
    return Response(status_code=204)

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
    # Conversión de porciones/día a porciones/semana para fruta, vegetales, papas fritas
    porciones_fruta_semana = int(consumo_fruta) * 7
    porciones_vegetales_semana = int(consumo_vegetales) * 7
    porciones_papas_semana = int(consumo_papas) * 7

    # El campo consumo_alcohol ya viene como unidades/semana según el formulario
    unidades_alcohol_semana = int(consumo_alcohol)

    # Construir DataFrame con los datos recibidos
    datos = {
        "Height_(cm)": altura,
        "Weight_(kg)": peso,
        "BMI": imc,
        "Alcohol_Consumption": unidades_alcohol_semana,
        "Fruit_Consumption": porciones_fruta_semana,
        "Green_Vegetables_Consumption": porciones_vegetales_semana,
        "FriedPotato_Consumption": porciones_papas_semana,
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
        consumo_alcohol=unidades_alcohol_semana,
        consumo_fruta=porciones_fruta_semana,
        consumo_vegetales=porciones_vegetales_semana,
        consumo_papas=porciones_papas_semana,
        salud_general=salud_general,  # valor numérico
        chequeo_medico=chequeo_medico,  # valor numérico
        ejercicio=ejercicio,  # valor numérico
        cancer_piel=cancer_piel,  # valor numérico
        otro_cancer=otro_cancer,  # valor numérico
        depresion=depresion,  # valor numérico
        diabetes=diabetes,  # valor numérico
        artritis=artritis,  # valor numérico
        sexo=sexo,  # valor numérico
        historial_tabaquismo=historial_tabaquismo,  # valor numérico
        edad=edad,
        resultado=prediccion,
        probabilidad=float(proba)  # Asegura tipo float nativo
    )
    db.add(registro)
    db.commit()
    db.close()

    return {
        "probabilidad": round(float(proba_mostrar), 3),
        "riesgo": "Alto" if prediccion == 1 else "Bajo",
        "mensaje": mensaje
    }
