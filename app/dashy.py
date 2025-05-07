import warnings
import dash
from dash import html, dcc, Input, Output, State
import requests
import os

# Suprimir advertencias de deprecación
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Configuración del backend
BACKEND_URL = "http://localhost:8000"
PREDICT_ENDPOINT = f"{BACKEND_URL}/api/v1/routes/predict"

# App initialization
app = dash.Dash(
    __name__,
    assets_folder='assets',
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="HeartWise - Riesgo Cardiaco",
    update_title=None
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

# Layout
app.layout = html.Div([
    html.Video(
        src='/assets/fondo_corazon.mp4', 
        autoPlay=True, 
        loop=True, 
        muted=True,
        style={
            'position': 'fixed',
            'width': '100%',
            'height': '100%',
            'objectFit': 'cover',
            'zIndex': '-1'
        }
    ),

    html.Div([
        html.H1("Evaluación de Riesgo Cardiovascular", className="titulo"),

        # Bloque general
        html.Div(id="bloque-general", className="formulario-bloque", children=[
            html.Label("Altura (cm)"),
            dcc.Input(id="altura", type="number", step="0.1", required=True, min=100, max=250),

            html.Label("Peso (kg)"),
            dcc.Input(id="peso", type="number", step="0.1", required=True, min=30, max=300),

            html.Label("IMC"),
            dcc.Input(id="imc", type="number", step="0.1", debounce=True, disabled=True),

            html.Label("Consumo de alcohol (veces/semana)"),
            dcc.Input(id="alcohol", type="number", min=0, max=7, required=True),

            html.Label("Consumo de fruta (porciones/semana)"),
            dcc.Input(id="fruta", type="number", min=0, max=21, required=True),

            html.Label("Consumo de vegetales verdes (porciones/semana)"),
            dcc.Input(id="verduras", type="number", min=0, max=21, required=True),

            html.Label("Consumo de papas fritas (porciones/semana)"),
            dcc.Input(id="papas", type="number", min=0, max=21, required=True),

            html.Div(
                "Es necesario completar todos los campos para poder realizar el estudio.",
                id="mensaje-aviso-1", 
                className="mensaje-aviso", 
                style={"display": "none"}
            ),
        ]),

        # Bloque médico
        html.Div(id="bloque-medico", className="formulario-bloque", style={"display": "none"}, children=[
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
                placeholder="Selecciona una opción"
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
                placeholder="Selecciona una opción"
            ),

            html.Label("¿Realiza ejercicio?"),
            dcc.Dropdown(
                id="ejercicio", 
                options=[
                    {"label": "Sí", "value": 1},
                    {"label": "No", "value": 0}
                ],
                placeholder="Selecciona una opción"
            ),

            html.Label("¿Antecedente de cáncer de piel?"),
            dcc.Dropdown(
                id="piel", 
                options=[
                    {"label": "Sí", "value": 1},
                    {"label": "No", "value": 0}
                ],
                placeholder="Selecciona una opción"
            ),

            html.Label("¿Antecedente de otro cáncer?"),
            dcc.Dropdown(
                id="cancer", 
                options=[
                    {"label": "Sí", "value": 1},
                    {"label": "No", "value": 0}
                ],
                placeholder="Selecciona una opción"
            ),

            html.Label("¿Depresión diagnosticada?"),
            dcc.Dropdown(
                id="depresion", 
                options=[
                    {"label": "Sí", "value": 1},
                    {"label": "No", "value": 0}
                ],
                placeholder="Selecciona una opción"
            ),

            html.Label("¿Diabetes?"),
            dcc.Dropdown(
                id="diabetes", 
                options=[
                    {"label": "No", "value": 0},
                    {"label": "No, pre-diabetes o borderline", "value": 1},
                    {"label": "Sí", "value": 2},
                    {"label": "Sí, solo durante embarazo", "value": 3}
                ],
                placeholder="Selecciona una opción"
            ),

            html.Label("¿Artritis?"),
            dcc.Dropdown(
                id="artritis", 
                options=[
                    {"label": "Sí", "value": 1},
                    {"label": "No", "value": 0}
                ],
                placeholder="Selecciona una opción"
            ),

            html.Label("Sexo"),
            dcc.Dropdown(
                id="sexo",
                options=[
                    {"label": "Masculino", "value": 0},
                    {"label": "Femenino", "value": 1}
                ],
                placeholder="Selecciona sexo"
            ),

            html.Label("Historial de tabaquismo"),
            dcc.Dropdown(
                id="historial_tabaquismo",
                options=[
                    {"label": "Sí", "value": 1},
                    {"label": "No", "value": 0}
                ],
                placeholder="Selecciona una opción"
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
                    {"label": "80 o más", "value": "80+"}
                ],
                placeholder="Selecciona rango de edad"
            ),
            
            html.Button("Evaluar Riesgo", id="submit-button", n_clicks=0, className="boton-evaluar"),
            html.Div(id="datos-para-enviar", style={"display": "none"})
        ]),

        # Resultados
        html.Div(id="resultado", className="resultado"),
    ], className="contenedor-form")
])

# Callbacks
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

@app.callback(
    Output("bloque-medico", "style"),
    Output("bloque-general", "style"),
    Output("mensaje-aviso-1", "style"),
    Input("altura", "value"),
    Input("peso", "value"),
    Input("imc", "value"),
    Input("alcohol", "value"),
    Input("fruta", "value"),
    Input("verduras", "value"),
    Input("papas", "value")
)
def validar_general(altura, peso, imc, alcohol, fruta, verduras, papas):
    if all(x is not None for x in [altura, peso, imc, alcohol, fruta, verduras, papas]):
        return {"display": "block"}, {"display": "none"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}, {"display": "block"}

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
    State("historial_tabaquismo", "value"),
)
def mostrar_resultado(n_clicks, altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
                     salud_general, chequeo, ejercicio, piel, cancer, depresion, diabetes, artritis, 
                     historial_tabaquismo):
    if not n_clicks:
        return "", ""
    
    campos = [altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
              salud_general, chequeo, ejercicio, piel, cancer, depresion, diabetes, artritis,
              historial_tabaquismo]
    
    if any(x is None for x in campos):
        return html.Div("Por favor, completa todos los campos antes de evaluar."), ""

    try:
        # Conversión explícita de tipos
        datos = {
            "altura": float(altura),
            "peso": float(peso),
            "imc": float(imc),
            "sexo": int(sexo),
            "edad": edad,
            "consumo_alcohol": int(alcohol),
            "consumo_fruta": int(fruta),
            "consumo_vegetales": int(verduras),
            "consumo_papas": int(papas),
            "salud_general": int(salud_general),
            "chequeo_medico": int(chequeo),
            "ejercicio": int(ejercicio),
            "cancer_piel": int(piel),
            "otro_cancer": int(cancer),
            "depresion": int(depresion),
            "diabetes": int(diabetes),
            "artritis": int(artritis),
            "historial_tabaquismo": int(historial_tabaquismo)
        }
    except (TypeError, ValueError) as e:
        return html.Div(f"Error en los datos: {str(e)}"), ""

    try:
        print(f"Enviando solicitud a: {PREDICT_ENDPOINT}")
        print(f"Datos enviados: {datos}")
        
        response = requests.post(
            PREDICT_ENDPOINT,
            json=datos,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Respuesta del servidor ({response.status_code}): {response.text}")
        
        if response.status_code != 200:
            return html.Div(f"Error del servidor: {response.text}"), ""

        resultado = response.json()

        # Validar estructura de respuesta
        if "prediction" not in resultado or "probability" not in resultado:
            return html.Div("Respuesta del servidor inválida"), ""

        riesgo_color = "red" if resultado["prediction"] == 1 else "green"
        mensaje = ("⚠️ Riesgo elevado de enfermedad cardíaca. Consulte a su médico." 
                  if resultado["prediction"] == 1 
                  else "✅ Bajo riesgo de enfermedad cardíaca.")
        
        return html.Div([
            html.H2("Resultado:", className="resultado-titulo"),
            html.P(f"Probabilidad: {round(resultado['probability']*100, 2)}%", className="resultado-probabilidad"),
            html.P(f"Riesgo: {'Alto' if resultado['prediction'] == 1 else 'Bajo'}", 
                  style={"color": riesgo_color, "font-weight": "bold"}, className="resultado-riesgo"),
            html.P(mensaje, className="resultado-mensaje")
        ]), ""

    except requests.exceptions.RequestException as e:
        error_msg = f"Error al conectar con el servidor: {str(e)}"
        if hasattr(e, 'response') and e.response:
            error_msg += f"\nDetalles: {e.response.text}"
        return html.Div(error_msg, className="error-mensaje"), ""

# Callback para mostrar cada bloque según el paso actual
@app.callback(
    Output("bloque-general", "style"),
    Output("bloque-habitos", "style"),
    Output("bloque-medico", "style"),
    Output("resultado", "style"),
    Input("next-1", "n_clicks"),
    Input("next-2", "n_clicks"),
    Input("back-2", "n_clicks"),
    Input("back-3", "n_clicks"),
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
)
def actualizar_pasos(n1, n2, b2, b3, submit,
                     altura, peso, imc, sexo, edad,
                     tabaquismo, alcohol, fruta, verduras,
                     salud_general, chequeo, ejercicio):
    triggered_id = ctx.triggered_id

    # Validación para avanzar del primer bloque
    if triggered_id == "next-1":
        if None in [altura, peso, imc, sexo, edad]:
            return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
        return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}

    # Validación para avanzar del segundo bloque
    elif triggered_id == "next-2":
        if None in [tabaquismo, alcohol, fruta, verduras]:
            return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}
        return {"display": "none"}, {"display": "none"}, {"display": "block"}, {"display": "none"}

    elif triggered_id == "back-2":
        return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif triggered_id == "back-3":
        return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}
    elif triggered_id == "submit-button":
        return {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "block"}

    return dash.no_update

if __name__ == "__main__":
    app.run(debug=True, port=8050)