import dash
from dash import html, dcc, Input, Output, State, ctx
import requests
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración del backend
BACKEND_URL = "http://localhost:8000"
PREDICT_ENDPOINT = f"{BACKEND_URL}/api/v1/routes/predict/"

# Inicialización de la app
app = dash.Dash(
    __name__,
    assets_folder='assets',
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="HeartWise - Riesgo Cardiaco",
    update_title=None,
    suppress_callback_exceptions=True
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

# Layout con bloques separados
app.layout = html.Div([
    # Video de fondo
    html.Video(src='/assets/fondo_corazon.mp4', autoPlay=True, loop=True, muted=True,
               className="video-background"),

    html.Div("HeartWise", className="navbar"),

    dcc.Store(id="current_step", data=0),
    dcc.Store(id="prediction_result", data=None),

    # Contenedor principal con scroll mejorado
    html.Div(className="main-container", style={
        'height': '85vh',
        'overflowY': 'auto',
        'paddingBottom': '100px'  # Espacio para los botones
    }, children=[
        # Bloque general
        html.Div(id="bloque-general", className="formulario-bloque bloque", children=[
            html.Label("Altura (cm)"),
            dcc.Input(id="altura", type="number", required=True),

            html.Label("Peso (kg)"),
            dcc.Input(id="peso", type="number", required=True),

            html.Label("IMC"),
            dcc.Input(id="imc", type="number", required=True, debounce=True, disabled=True),

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

            html.Button("Siguiente", id="next-1", n_clicks=0, className="form-button"),
        ], style={"display": "block"}),

        # Bloque hábitos
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

            html.Label("Consumo de papas fritas (porciones/semana)"),
            dcc.Input(id="papas", type="number", min=0, max=100, required=True),

            html.Div(className="button-group", children=[
                html.Button("Atrás", id="back-2", n_clicks=0, className="form-button"),
                html.Button("Siguiente", id="next-2", n_clicks=0, className="form-button"),
            ]),
        ], style={"display": "none"}),

        # Bloque médico
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
            
            html.Label("Cáncer de piel"),
            dcc.Dropdown(
                id="cancer_piel", 
                options=[{"label": "Sí", "value": 1}, {"label": "No", "value": 0}],
                placeholder="Selecciona"
            ),
          
            html.Label("Otro cáncer"),
            dcc.Dropdown(
                id="otro_cancer", 
                options=[{"label": "Sí", "value": 1}, {"label": "No", "value": 0}],
                placeholder="Selecciona"
            ),

            html.Label("Depresión"),
            dcc.Dropdown(
                id="depresion", 
                options=[{"label": "Sí", "value": 1}, {"label": "No", "value": 0}],
                placeholder="Selecciona"
            ),

            html.Label("Diabetes"),
            dcc.Dropdown(
                id="diabetes", 
                options=[
                    {"label": "No", "value": 0},
                    {"label": "Pre-diabetes", "value": 1},
                    {"label": "Sí", "value": 2},
                    {"label": "Solo en embarazo", "value": 3}
                ],
                placeholder="Selecciona"
            ),

            html.Label("Artritis"),
            dcc.Dropdown(
                id="artritis", 
                options=[{"label": "Sí", "value": 1}, {"label": "No", "value": 0}],
                placeholder="Selecciona"
            ),

            # Botones dentro del bloque con margen superior
            html.Div(className="button-group", style={"marginTop": "40px", "marginBottom": "40px"}, children=[
                html.Button("Atrás", id="back-3", n_clicks=0, className="form-button"),
                html.Button("Evaluar Riesgo", id="submit-button", n_clicks=0, className="form-button primary"),
            ]),
        ], style={"display": "none"}),

        # Resultados
        html.Div(id="resultado", className="resultado", style={"display": "none"}, children=[
            html.Div(id="mensaje-resultado", className="mensaje-resultado"),
            html.Div(className="button-group", style={"marginTop": "20px"}, children=[
                html.Button("Realizar una nueva predicción", id="nueva-prediccion", n_clicks=0, className="form-button"),
                html.Button("Finalizar predicción", id="finalizar-prediccion", n_clicks=0, className="form-button primary"),
            ]),
        ]),

        # Finalización
        html.Div(id="finalizacion", className="resultado", style={"display": "none"}, children=[
            html.H2("¡Muchas gracias por elegirnos!"),
            html.P("Tenga un excelente día."),
            html.Button("Volver a inicio", id="volver-inicio", n_clicks=0, className="form-button"),
        ]),
    ]),

    html.Div("© 2025 HeartWise", className="footer")
])

# Callback para actualizar IMC
@app.callback(
    Output("imc", "value"),
    Input("altura", "value"),
    Input("peso", "value"),
    prevent_initial_call=True
)
def actualizar_imc(altura, peso):
    if altura and peso and altura > 0:
        altura_m = altura / 100
        return round(peso / (altura_m ** 2), 2)
    return None

# Callback para navegación entre pasos
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
    State("papas", "value"),
    State("salud_general", "value"),
    State("chequeo", "value"),
    State("ejercicio", "value"),
)
def actualizar_pasos(n1, n2, b2, b3, submit, nueva_pred, finalizar_pred, volver_inicio,
                     altura, peso, imc, sexo, edad, tabaquismo, alcohol, fruta, verduras, papas,
                     salud_general, chequeo, ejercicio):
    triggered_id = ctx.triggered_id if ctx.triggered_id is not None else ""

    # Validación para avanzar del primer bloque
    if triggered_id == "next-1":
        if None in [altura, peso, imc, sexo, edad]:
            return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
        return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}

    # Validación para avanzar del segundo bloque
    elif triggered_id == "next-2":
        if None in [tabaquismo, alcohol, fruta, verduras, papas]:
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

# Callback para enviar datos a la API y mostrar resultados
# ... (todo el código anterior permanece igual hasta el callback mostrar_resultado)

@app.callback(
    Output("mensaje-resultado", "children"),
    Output("prediction_result", "data"),
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
    State("cancer_piel", "value"),
    State("otro_cancer", "value"),
    State("depresion", "value"),
    State("diabetes", "value"),
    State("artritis", "value"),
    State("tabaquismo", "value"),
    prevent_initial_call=True
)
def mostrar_resultado(n_clicks, altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
                     salud_general, chequeo, ejercicio, cancer_piel, otro_cancer, depresion, 
                     diabetes, artritis, tabaquismo):
    
    if None in [altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
                salud_general, chequeo, ejercicio, cancer_piel, otro_cancer, depresion,
                diabetes, artritis, tabaquismo]:
        return "Por favor, completa todos los campos antes de evaluar el riesgo.", None

    # Preparar los datos para enviar a la API en el orden correcto
    datos = {
        "altura": float(altura),
        "peso": float(peso),
        "imc": float(imc),
        "sexo": int(sexo),
        "edad": edad,
        "consumo_alcohol": int(alcohol),
        "consumo_fruta": int(fruta) * 7,  # Convertir a semanal
        "consumo_vegetales": int(verduras) * 7,  # Convertir a semanal
        "consumo_papas": int(papas),
        "salud_general": int(salud_general),
        "chequeo_medico": int(chequeo),
        "ejercicio": int(ejercicio),
        "cancer_piel": int(cancer_piel),
        "otro_cancer": int(otro_cancer),
        "depresion": int(depresion),
        "diabetes": int(diabetes),
        "artritis": int(artritis),
        "historial_tabaquismo": int(tabaquismo)
    }

    try:
        logger.info(f"Enviando datos a la API: {datos}")
        response = requests.post(
            PREDICT_ENDPOINT,
            json=datos,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code != 200:
            logger.error(f"Error en la respuesta de la API: {response.status_code} - {response.text}")
            return f"Error al conectar con el servidor: {response.text}", None

        resultado = response.json()
        logger.info(f"Respuesta recibida de la API: {resultado}")

        if "prediction" not in resultado or "probability" not in resultado:
            return "Respuesta del servidor inválida", None

        prediccion = resultado["prediction"]

        # Mensaje simplificado sin porcentaje
        if prediccion == 1:
            mensaje = html.Div([
                html.H3("⚠️ Riesgo elevado de enfermedad cardíaca", className="high-risk"),
                html.P("Consulte a su médico de cabecera para derivación a Cardiología.", className="resultado-mensaje")
            ])
        else:
            mensaje = html.Div([
                html.H3("✅ Bajo riesgo de enfermedad cardíaca", className="low-risk"),
                html.P("Mantenga sus controles médicos regulares.", className="resultado-mensaje")
            ])

        return mensaje, {"mensaje": mensaje, "probabilidad": float(resultado["probability"])}

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión: {str(e)}")
        return f"Error al conectar con el servidor: {str(e)}", None
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return f"Error inesperado: {str(e)}", None


# Callback para resetear el formulario
@app.callback(
    [Output(field, "value", allow_duplicate=True) if field == "imc" else Output(field, "value") 
     for field in ["altura", "peso", "imc", "sexo", "edad", 
                  "tabaquismo", "alcohol", "fruta", "verduras", "papas",
                  "salud_general", "chequeo", "ejercicio",
                  "cancer_piel", "otro_cancer", "depresion", "diabetes", "artritis"]],
    Input("nueva-prediccion", "n_clicks"),
    Input("volver-inicio", "n_clicks"),
    prevent_initial_call=True
)
def reset_form(nueva_pred, volver_inicio):
    return [None] * 18  # Resetear todos los campos

if __name__ == "__main__":
    logger.info("Iniciando aplicación HeartWise con conexión a API...")
    # app.run(debug=True)
    app.run(debug=True, host="0.0.0.0", port=8050)