import dash
from dash import html, dcc, Input, Output, State, ctx
import requests
import dash_daq as daq
import pandas as pd
import joblib
import os
from db.db import SessionLocal
from models.models import Prediccion

# App initialization
app = dash.Dash(
    __name__,
    assets_folder='assets',
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="Riesgo Cardiaco",
    update_title=None
)
app._favicon = "heart.png"
server = app.server

# Helper functions
def calcular_imc(peso, altura_cm):
    try:
        altura_m = altura_cm / 100
        return round(peso / (altura_m ** 2), 2)
    except:
        return None

# Cargar modelo y parámetros
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
MODELS_PATH = os.path.join(BASE_PATH, "models_pkl")
modelo_lda = joblib.load(os.path.join(MODELS_PATH, "modelo_predictor_enfermedad_cardiaca.pkl"))
info_modelo = joblib.load(os.path.join(MODELS_PATH, "info_modelo_cardiaco.pkl"))
umbral_optimo = info_modelo["umbral_optimo"]
variables_modelo = info_modelo["variables"]

# Layout
app.layout = html.Div([

    html.Video(src='/assets/fondo_corazon.mp4', autoPlay=True, loop=True, muted=True,
               style={
                   'position': 'fixed',
                   'width': '100%',
                   'height': '100%',
                   'objectFit': 'cover',
                   'zIndex': '-1'
               }),

    html.Div([

        html.H1("Evaluación de Riesgo Cardiovascular", className="titulo"),

        html.Div(id="bloque-general", className="formulario-bloque", children=[
            html.Label("Altura (cm)"),
            dcc.Input(id="altura", type="number", required=True),

            html.Label("Peso (kg)"),
            dcc.Input(id="peso", type="number", required=True),

            html.Label("IMC"),
            dcc.Input(id="imc", type="number", required=True, debounce=True),

            html.Label("Sexo"),
            dcc.Dropdown(
                id="sexo",
                options=[
                    {"label": "Masculino", "value": 0},
                    {"label": "Femenino", "value": 1}
                ],
                placeholder="Selecciona sexo"
            ),

            html.Label("Edad"),
            dcc.Input(id="edad", type="number", required=True),

            html.Div("Es necesario completar todos los campos para poder realizar el estudio.",
                     id="mensaje-aviso-1", className="mensaje-aviso", style={"display": "none"}),

        ]),

        html.Div(id="bloque-habitos", className="formulario-bloque", style={"display": "none"}, children=[
            html.Label("Consumo de alcohol (0 no / 1 sí)"),
            dcc.Dropdown(id="alcohol", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Label("Fruta diaria (0 no / 1 sí)"),
            dcc.Dropdown(id="fruta", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Label("Vegetales verdes (0 no / 1 sí)"),
            dcc.Dropdown(id="verduras", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Label("Papas fritas (0 no / 1 sí)"),
            dcc.Dropdown(id="papas", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Div("Es necesario completar todos los campos para poder continuar.",
                     id="mensaje-aviso-2", className="mensaje-aviso", style={"display": "none"}),
        ]),

        html.Div(id="bloque-medico", className="formulario-bloque", style={"display": "none"}, children=[
            html.Label("Salud general (1-5)"),
            dcc.Slider(id="salud_general", min=1, max=5, step=1, marks={i: str(i) for i in range(1, 6)}),

            html.Label("Chequeo médico reciente (0 no / 1 sí)"),
            dcc.Dropdown(id="chequeo", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Label("Ejercicio (0 no / 1 sí)"),
            dcc.Dropdown(id="ejercicio", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Label("Cáncer de piel"),
            dcc.Dropdown(id="piel", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Label("Otro cáncer"),
            dcc.Dropdown(id="cancer", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Label("Depresión"),
            dcc.Dropdown(id="depresion", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Label("Diabetes"),
            dcc.Dropdown(id="diabetes", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Label("Artritis"),
            dcc.Dropdown(id="artritis", options=[{"label": str(i), "value": i} for i in [0, 1]]),

            html.Div(id="datos-para-enviar"),        
            html.Button("Evaluar Riesgo", id="submit-button", n_clicks=0)
        ]),

        html.Div(id="resultado", className="resultado"),

    ], className="contenedor-form")
])

# Cálculo automático del IMC
@app.callback(
    Output("imc", "value"),
    Input("peso", "value"),
    Input("altura", "value"),
    State("imc", "value")
)
def calcular_imc_autom(peso, altura, imc_actual):
    if peso and altura and not imc_actual:
        return calcular_imc(peso, altura)
    return dash.no_update

# Validación y transición entre bloques
@app.callback(
    Output("bloque-habitos", "style"),
    Output("bloque-general", "style"),
    Output("mensaje-aviso-1", "style"),
    Input("altura", "value"),
    Input("peso", "value"),
    Input("imc", "value"),
    Input("sexo", "value"),
    Input("edad", "value")
)
def validar_general(altura, peso, imc, sexo, edad):
    if all(x is not None for x in [altura, peso, imc, sexo, edad]):
        return {"display": "block"}, {"display": "none"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}, {"display": "block"}

@app.callback(
    Output("bloque-medico", "style"),
    Output("mensaje-aviso-2", "style"),
    Input("alcohol", "value"),
    Input("fruta", "value"),
    Input("verduras", "value"),
    Input("papas", "value")
)
def validar_habitos(alcohol, fruta, verduras, papas):
    if all(x is not None for x in [alcohol, fruta, verduras, papas]):
        return {"display": "block"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}

# Resultado de predicción
@app.callback(
    Output("resultado", "children"),
    Output("datos-para-enviar", "children"),
    Input("submit-button", "n_clicks"),
    State("altura", "value"),
    State("peso", "value"),
    State("imc", "value"),
    State("sexo", "value"),
    State("edad", "value"),
    State("alcohol", "value"),
    State("fruta", "value"),
    State("verduras", "value"),
    State("papas", "value"),
    State("salud_general", "value"),
    State("chequeo", "value"),
    State("ejercicio", "value"),
    State("piel", "value"),
    State("cancer", "value"),
    State("depresion", "value"),
    State("diabetes", "value"),
    State("artritis", "value"),
)
def mostrar_resultado(n_clicks, altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
                     salud_general, chequeo, ejercicio, piel, cancer, depresion, diabetes, artritis):
    if not n_clicks:
        return "", ""
    campos = [altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
              salud_general, chequeo, ejercicio, piel, cancer, depresion, diabetes, artritis]
    if any(x is None for x in campos):
        return html.Div("Por favor, completa todos los campos antes de evaluar."), ""
    # Procesar datos
    datos = {
        "Height_(cm)": altura,
        "Weight_(kg)": peso,
        "BMI": imc,
        "Alcohol_Consumption": alcohol,
        "Fruit_Consumption": fruta,
        "Green_Vegetables_Consumption": verduras,
        "FriedPotato_Consumption": papas,
        "General_Health": salud_general,
        "Checkup": chequeo,
        "Exercise": ejercicio,
        "Skin_Cancer": piel,
        "Other_Cancer": cancer,
        "Depression": depresion,
        "Diabetes": diabetes,
        "Arthritis": artritis,
        "Sex": sexo,
        "Smoking_History": 0,
        "Age_Category": str(edad)
    }
    df = pd.DataFrame([datos])
    df_age_cat = pd.get_dummies(df["Age_Category"], prefix="Age_Category")
    df = df.drop(["Age_Category"], axis=1)
    X_nuevo = pd.concat([df, df_age_cat], axis=1)
    for col in variables_modelo:
        if col not in X_nuevo.columns:
            X_nuevo[col] = 0
    X_nuevo = X_nuevo[variables_modelo]
    proba = modelo_lda.predict_proba(X_nuevo)[:, 1][0]
    prediccion = int(proba > umbral_optimo)
    if prediccion == 1:
        mensaje = "⚠️ Riesgo elevado de enfermedad cardíaca. Consulte a su médico de cabecera para derivación a Cardiología."
    else:
        mensaje = "✅ Bajo riesgo de enfermedad cardíaca. Mantenga sus controles médicos regulares."
    # Guardar en base de datos
    db = SessionLocal()
    registro = Prediccion(
        altura=altura,
        peso=peso,
        imc=imc,
        consumo_alcohol=alcohol,
        consumo_fruta=fruta,
        consumo_vegetales=verduras,
        consumo_papas=papas,
        salud_general=salud_general,
        chequeo_medico=chequeo,
        ejercicio=ejercicio,
        cancer_piel=piel,
        otro_cancer=cancer,
        depresion=depresion,
        diabetes=diabetes,
        artritis=artritis,
        sexo=sexo,
        historial_tabaquismo=0,
        edad=str(edad),
        resultado=prediccion,
        probabilidad=proba
    )
    db.add(registro)
    db.commit()
    db.close()
    # Mostrar resultado
    return html.Div([
        html.H2("Resultado:"),
        html.P(f"Probabilidad de enfermedad cardíaca: {round(proba*100)}%"),
        html.P(f"Riesgo: {'Alto' if prediccion == 1 else 'Bajo'}"),
        html.P(mensaje)
    ]), ""

if __name__ == "__main__":
    app.run(debug=True)