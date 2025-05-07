import dash
from dash import html, dcc, Input, Output, State, ctx
import joblib
import os
from db.db import SessionLocal
from models.models import Prediccion

# Inicialización de la app
app = dash.Dash(
    __name__,
    assets_folder='assets',
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="HeartWise - Riesgo Cardiaco",
    update_title=None,
    suppress_callback_exceptions=True  # Added this parameter to fix the callback exceptions
)
app._favicon = "heart.png"
server = app.server

# Función para calcular el IMC
def calcular_imc(peso, altura_cm):
    try:
        altura_m = altura_cm / 100
        return round(peso / (altura_m ** 2), 2)
    except:
        return None

@app.callback(
    Output("imc", "value"),
    Input("altura", "value"),
    Input("peso", "value"),
    prevent_initial_call=True
)
def actualizar_imc(altura, peso):
    if altura and peso and altura > 0:  # Añadida validación para evitar división por cero
        altura_m = altura / 100  # Convertir cm a metros
        return round(peso / (altura_m ** 2), 2)
    return None

# Cargar modelo y parámetros
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
MODELS_PATH = os.path.join(BASE_PATH, "models_pkl")
modelo_lda = joblib.load(os.path.join(MODELS_PATH, "modelo_predictor_enfermedad_cardiaca.pkl"))
info_modelo = joblib.load(os.path.join(MODELS_PATH, "info_modelo_cardiaco.pkl"))
umbral_optimo = info_modelo["umbral_optimo"]
variables_modelo = info_modelo["variables"]

# Layout con bloques separados
app.layout = html.Div([

    # Video de fondo
    html.Video(src='/assets/fondo_corazon.mp4', autoPlay=True, loop=True, muted=True,
               className="video-background"),

    html.Div("HeartWise", className="navbar"),

    dcc.Store(id="current_step", data=0),  # Control de pasos
    dcc.Store(id="prediction_result", data=None),  # Para almacenar resultado de predicción

    html.Div(id="bloque-general", className="formulario-bloque bloque", children=[
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
        dcc.Dropdown(
            id="edad",
            options=[
                {"label": "18-24", "value": "18-24"},
                {"label": "25-29", "value": "25-29"},
                {"label": "30-34", "value": "30-34"},
                {"label": "35-39", "value": "35-39"},
                {"label": "40-44", "value": "40-44"},
                {"label": "45-49", "value": "45-49"},
                {"label": "50-54", "value": "50-54"},
                {"label": "55-59", "value": "55-59"},
                {"label": "60-64", "value": "60-64"},
                {"label": "65-69", "value": "65-69"},
                {"label": "70-74", "value": "70-74"},
                {"label": "75-79", "value": "75-79"},
                {"label": "80+", "value": "80+"}
            ],
            placeholder="Selecciona edad"
        ),

        html.Button("Siguiente", id="next-1", n_clicks=0),
    ], style={"display": "block"}),

    html.Div(id="bloque-habitos", className="formulario-bloque bloque", children=[
        html.Label("Historial de tabaquismo"),
        dcc.Dropdown(
            id="tabaquismo",
            options=[
                {"label": "Sí", "value": 1},
                {"label": "No", "value": 0}
            ],
            placeholder="Selecciona"
        ),

        html.Label("Consumo de alcohol (frecuencia)"),
        dcc.Dropdown(
            id="alcohol",
            options=[
                {"label": "Ninguna", "value": 0},
                {"label": "Ocasional (1/semana)", "value": 1},
                {"label": "1 vez al día", "value": 7},
                {"label": "2 veces al día", "value": 14},
                {"label": "3 veces al día", "value": 21},
                {"label": "4-5 veces al día", "value": 30}
            ],
            placeholder="Selecciona"
        ),

        html.Label("Consumo de fruta (porciones/día)"),
        dcc.Dropdown(
            id="fruta",
            options=[
                {"label": str(i), "value": i} for i in [0, 1, 2, 3, 4, 9, 13, 17, 18]
            ],
            placeholder="Selecciona"
        ),

        html.Label("Consumo de vegetales verdes (porciones/día)"),
        dcc.Dropdown(
            id="verduras",
            options=[
                {"label": str(i), "value": i} for i in [0, 1, 2, 3, 4, 9, 13, 17, 18]
            ],
            placeholder="Selecciona"
        ),

        html.Button("Atrás", id="back-2", n_clicks=0),
        html.Button("Siguiente", id="next-2", n_clicks=0),
    ], style={"display": "none"}),

    html.Div(id="bloque-medico", className="formulario-bloque bloque", children=[
        html.Label("Salud general"),
        dcc.Dropdown(
            id="salud_general",
            options=[
                {"label": "Mala", "value": 0},
                {"label": "Regular", "value": 1},
                {"label": "Buena", "value": 2},
                {"label": "Muy buena", "value": 3},
                {"label": "Excelente", "value": 4}
            ],
            placeholder="Selecciona"
        ),

        html.Label("Chequeo médico"),
        dcc.Dropdown(
            id="chequeo",
            options=[
                {"label": "Nunca", "value": 0},
                {"label": "Hace 5 años o más", "value": 1},
                {"label": "En los últimos 5 años", "value": 2},
                {"label": "En los últimos 2 años", "value": 3},
                {"label": "En el último año", "value": 4}
            ],
            placeholder="Selecciona"
        ),

        html.Label("Ejercicio"),
        dcc.Dropdown(
            id="ejercicio",
            options=[
                {"label": "Sí", "value": 1},
                {"label": "No", "value": 0}
            ],
            placeholder="Selecciona"
        ),

        html.Button("Atrás", id="back-3", n_clicks=0),
        html.Button("Evaluar Riesgo", id="submit-button", n_clicks=0),
    ], style={"display": "none"}),

    html.Div(id="resultado", className="resultado", style={"display": "none"}, children=[
        html.Div(id="mensaje-resultado", className="mensaje-resultado"),
        html.Div(className="botones-accion", children=[
            html.Button("Realizar una nueva predicción", id="nueva-prediccion", n_clicks=0, className="btn-accion"),
            html.Button("Finalizar predicción", id="finalizar-prediccion", n_clicks=0, className="btn-accion")
        ]),
    ]),

    # Bloque para mensaje de finalización
    html.Div(id="finalizacion", className="resultado", style={"display": "none"}, children=[
        html.H2("¡Gracias por utilizar HeartWise!"),
        html.P("Su análisis ha sido completado."),
        html.Button("Volver a inicio", id="volver-inicio", n_clicks=0),
    ]),

    html.Div("© 2025 HeartWise", className="footer")
])

# Callback para mostrar cada bloque según el paso actual
@app.callback(
    Output("bloque-general", "style"),
    Output("bloque-habitos", "style"),
    Output("bloque-medico", "style"),
    Output("resultado", "style"),
    Output("finalizacion", "style"),
    Input("next-1", "n_clicks"),
    Input("next-2", "n_clicks"),
    Input("back-2", "n_clicks"),
    Input("back-3", "n_clicks"),
    Input("submit-button", "n_clicks"),
    Input("nueva-prediccion", "n_clicks"),
    Input("finalizar-prediccion", "n_clicks"),
    Input("volver-inicio", "n_clicks"),
    State("altura", "value"),
    State("peso", "value"),
    State("imc", "value"),
    State("sexo", "value"),
    State("edad", "value"),
    State("tabaquismo", "value"),
    State("alcohol", "value"),
    State("fruta", "value"),
    State("verduras", "value"),
    State("salud_general", "value"),
    State("chequeo", "value"),
    State("ejercicio", "value"),
)
def actualizar_pasos(n1, n2, b2, b3, submit, nueva_pred, finalizar_pred, volver_inicio,
                     altura, peso, imc, sexo, edad,
                     tabaquismo, alcohol, fruta, verduras,
                     salud_general, chequeo, ejercicio):
    # Manejo robusto del trigger
    triggered_id = ctx.triggered_id if ctx.triggered_id is not None else ""

    # Validación para avanzar del primer bloque
    if triggered_id == "next-1":
        if None in [altura, peso, imc, sexo, edad]:
            return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
        return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}

    # Validación para avanzar del segundo bloque
    elif triggered_id == "next-2":
        if None in [tabaquismo, alcohol, fruta, verduras]:
            return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
        return {"display": "none"}, {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}

    elif triggered_id == "back-2":
        return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif triggered_id == "back-3":
        return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif triggered_id == "submit-button":
        return {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "block"}, {"display": "none"}
    elif triggered_id == "nueva-prediccion":
        return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif triggered_id == "finalizar-prediccion":
        return {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "block"}
    elif triggered_id == "volver-inicio":
        return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}

    # Por defecto, mostrar solo el primer bloque
    return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}

@app.callback(
    Output("resultado", "children"),
    Output("prediction_result", "data"),
    Input("submit-button", "n_clicks"),
    State("altura", "value"),
    State("peso", "value"),
    State("imc", "value"),
    State("sexo", "value"),
    State("edad", "value"),
    State("tabaquismo", "value"),
    State("alcohol", "value"),
    State("fruta", "value"),
    State("verduras", "value"),
    State("salud_general", "value"),
    State("chequeo", "value"),
    State("ejercicio", "value"),
    prevent_initial_call=True
)
def mostrar_resultado(n_clicks, altura, peso, imc, sexo, edad,
                      tabaquismo, alcohol, fruta, verduras,
                      salud_general, chequeo, ejercicio):
    if None in [altura, peso, imc, sexo, edad, tabaquismo, alcohol, fruta, verduras, salud_general, chequeo, ejercicio]:
        return "Por favor, completa todos los campos antes de evaluar el riesgo.", None

    import pandas as pd

    # Prepara los datos igual que en tu modelo
    datos = {
        "Height_(cm)": altura,
        "Weight_(kg)": peso,
        "BMI": imc,
        "Alcohol_Consumption": alcohol,
        "Fruit_Consumption": fruta * 7,
        "Green_Vegetables_Consumption": verduras * 7,
        "FriedPotato_Consumption": 0,  # Si no tienes este campo, pon 0
        "General_Health": salud_general,
        "Checkup": chequeo,
        "Exercise": ejercicio,
        "Skin_Cancer": 0,
        "Other_Cancer": 0,
        "Depression": 0,
        "Diabetes": 0,
        "Arthritis": 0,
        "Sex": sexo,
        "Smoking_History": tabaquismo,
        "Age_Category": edad
    }
    df = pd.DataFrame([datos])
    df_age_cat = pd.get_dummies(df["Age_Category"], prefix="Age_Category")
    df = df.drop(["Age_Category"], axis=1)
    X_nuevo = pd.concat([df, df_age_cat], axis=1)
    for col in variables_modelo:
        if col not in X_nuevo.columns:
            X_nuevo[col] = 0
    X_nuevo = X_nuevo[variables_modelo]

    prob = modelo_lda.predict_proba(X_nuevo)[0][1]
    prediccion = int(prob > umbral_optimo)
    
    # Guardar resultado en BD (si es necesario)
    try:
        db = SessionLocal()
        nueva_prediccion = Prediccion(
            altura=altura, peso=peso, imc=imc,
            sexo=sexo, edad=edad, tabaquismo=tabaquismo,
            alcohol=alcohol, fruta=fruta, verduras=verduras,
            salud_general=salud_general, chequeo=chequeo,
            ejercicio=ejercicio, probabilidad=float(prob),
            prediccion=prediccion
        )
        db.add(nueva_prediccion)
        db.commit()
    except Exception as e:
        print(f"Error al guardar en BD: {e}")
    finally:
        if 'db' in locals():
            db.close()
    
    if prediccion == 1:
        mensaje = "⚠️ Riesgo elevado de enfermedad cardíaca. Consulte a su médico de cabecera para derivación a Cardiología."
    else:
        mensaje = "✅ Bajo riesgo de enfermedad cardíaca. Mantenga sus controles médicos regulares."
    
    # Usar el div existente en lugar de crear uno nuevo
    resultado = html.Div([
        html.Div(mensaje, className="mensaje-resultado"),
    ])
    
    return resultado, {"mensaje": mensaje, "probabilidad": float(prob)}

# Reset callback para limpiar los campos al iniciar nueva predicción
@app.callback(
    [Output(field, "value", allow_duplicate=True) if field == "imc" else Output(field, "value") 
     for field in ["altura", "peso", "imc", "sexo", "edad", 
                  "tabaquismo", "alcohol", "fruta", "verduras",
                  "salud_general", "chequeo", "ejercicio"]],
    Input("nueva-prediccion", "n_clicks"),
    Input("volver-inicio", "n_clicks"),
    prevent_initial_call=True
)
def reset_form(nueva_pred, volver_inicio):
    # Resetear todos los campos a None
    return [None] * 12

if __name__ == "__main__":
    app.run(debug=True)
