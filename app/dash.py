# import dash
# from dash import html, dcc, Input, Output, State, ctx
# import joblib
# import os
# import pandas as pd
# from db.db import SessionLocal
# from models.models import Prediccion

# # Inicialización de la app
# app = dash.Dash(
#     __name__,
#     assets_folder='assets',
#     meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
#     title="HeartWise - Riesgo Cardiaco",
#     update_title=None
# )
# app._favicon = "heart.png"
# server = app.server

# # Función para calcular el IMC
# def calcular_imc(peso, altura_cm):
#     try:
#         altura_m = altura_cm / 100
#         return round(peso / (altura_m ** 2), 2)
#     except:
#         return None

# # Cargar modelo y parámetros
# BASE_PATH = os.path.dirname(os.path.dirname(__file__))
# MODELS_PATH = os.path.join(BASE_PATH, "models_pkl")
# modelo_lda = joblib.load(os.path.join(MODELS_PATH, "modelo_predictor_enfermedad_cardiaca.pkl"))
# info_modelo = joblib.load(os.path.join(MODELS_PATH, "info_modelo_cardiaco.pkl"))
# umbral_optimo = info_modelo["umbral_optimo"]
# variables_modelo = info_modelo["variables"]

# # Layout con bloques separados
# app.layout = html.Div([

#     # Video de fondo
#     html.Video(src='/assets/fondo_corazon.mp4', autoPlay=True, loop=True, muted=True, className="video-background"),

#     html.Div("HeartWise", className="navbar"),

#     dcc.Store(id="current_step", data=0),  # Control de pasos

#     # Bloque 1: Información General
#     html.Div(id="bloque-general", className="formulario-bloque bloque", children=[
#         html.H3("Información General"),
#         html.Label("Altura (cm)"),
#         dcc.Input(id="altura", type="number", required=True),

#         html.Label("Peso (kg)"),
#         dcc.Input(id="peso", type="number", required=True),

#         html.Label("IMC"),
#         dcc.Input(id="imc", type="number", required=True, debounce=True),

#         html.Label("Sexo"),
#         dcc.Dropdown(id="sexo", options=[{"label": "Masculino", "value": 0}, {"label": "Femenino", "value": 1}],
#                      placeholder="Selecciona sexo"),

#         html.Label("Edad"),
#         dcc.Input(id="edad", type="number", required=True),

#         html.Button("Siguiente", id="next-1", n_clicks=0),
#     ], style={"display": "block"}),  

#     # Bloque 2: Hábitos
#     html.Div(id="bloque-habitos", className="formulario-bloque bloque", children=[
#         html.H3("Hábitos de vida"),
#         html.Label("Historial de tabaquismo"),
#         dcc.Dropdown(id="tabaquismo", options=[{"label": "Sí", "value": 1}, {"label": "No", "value": 0}]),

#         html.Label("Consumo de alcohol (veces/semana)"),
#         dcc.Input(id="alcohol", type="number"),

#         html.Label("Consumo de fruta (porciones/semana)"),
#         dcc.Input(id="fruta", type="number"),

#         html.Label("Consumo de vegetales verdes (porciones/semana)"),
#         dcc.Input(id="verduras", type="number"),

#         html.Button("Atrás", id="back-2", n_clicks=0),
#         html.Button("Siguiente", id="next-2", n_clicks=0),
#     ], style={"display": "none"}),  

#     # Bloque 3: Datos Médicos
#     html.Div(id="bloque-medico", className="formulario-bloque bloque", children=[
#         html.H3("Historial Médico"),
#         html.Label("Salud general (1-5)"),
#         dcc.Slider(id="salud_general", min=1, max=5, step=1, marks={i: str(i) for i in range(1, 6)}),

#         html.Label("Chequeo médico reciente"),
#         dcc.Dropdown(id="chequeo", options=[{"label": "Sí", "value": 1}, {"label": "No", "value": 0}]),

#         html.Label("Ejercicio"),
#         dcc.Dropdown(id="ejercicio", options=[{"label": "Sí", "value": 1}, {"label": "No", "value": 0}]),

#         html.Button("Atrás", id="back-3", n_clicks=0),
#         html.Button("Evaluar Riesgo", id="submit-button", n_clicks=0),
#     ], style={"display": "none"}),  

#     # Bloque 4: Predicción
#     html.Div(id="resultado", className="resultado", style={"display": "none"}),

#     html.Div("© 2025 HeartWise", className="footer")
# ])

# # Callback para manejar la transición de los bloques
# @app.callback(
#     Output("bloque-general", "style"),
#     Output("bloque-habitos", "style"),
#     Output("bloque-medico", "style"),
#     Output("resultado", "style"),
#     Input("next-1", "n_clicks"),
#     Input("next-2", "n_clicks"),
#     Input("back-2", "n_clicks"),
#     Input("back-3", "n_clicks"),
#     Input("submit-button", "n_clicks"),
#     State("current_step", "data")
# )
# def actualizar_pasos(n1, n2, b2, b3, submit, paso):
#     triggered_id = ctx.triggered_id

#     if triggered_id == "next-1":
#         return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}
#     elif triggered_id == "next-2":
#         return {"display": "none"}, {"display": "none"}, {"display": "block"}, {"display": "none"}
#     elif triggered_id == "back-2":
#         return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
#     elif triggered_id == "back-3":
#         return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}
#     elif triggered_id == "submit-button":
#         return {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "block"}
    
#     return dash.no_update

# if __name__ == "__main__":
#     app.run(debug=True)
