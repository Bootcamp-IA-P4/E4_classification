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

def convertir_rango_edad(edad_num):
    try:
        edad = int(edad_num)
        if edad < 18:
            return "18-24"
        elif 18 <= edad <= 24:
            return "18-24"
        elif 25 <= edad <= 29:
            return "25-29"
        elif 30 <= edad <= 34:
            return "30-34"
        elif 35 <= edad <= 39:
            return "35-39"
        elif 40 <= edad <= 44:
            return "40-44"
        elif 45 <= edad <= 49:
            return "45-49"
        elif 50 <= edad <= 54:
            return "50-54"
        elif 55 <= edad <= 59:
            return "55-59"
        elif 60 <= edad <= 64:
            return "60-64"
        elif 65 <= edad <= 69:
            return "65-69"
        elif 70 <= edad <= 74:
            return "70-74"
        elif 75 <= edad <= 79:
            return "75-79"
        else:
            return "80+"
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
            dcc.Input(id="altura", type="number", required=True, min=100, max=250),

            html.Label("Peso (kg)"),
            dcc.Input(id="peso", type="number", required=True, min=30, max=300),

            html.Label("IMC"),
            dcc.Input(id="imc", type="number", debounce=True, disabled=True),

            html.Label("Sexo"),
            dcc.Dropdown(
                id="sexo",
                options=[
                    {"label": "Masculino", "value": 1},
                    {"label": "Femenino", "value": 0}
                ],
                placeholder="Selecciona sexo"
            ),

            html.Label("Edad (número entero)"),
            dcc.Input(
                id="edad", 
                type="number", 
                required=True,
                min=18,
                max=120,
                placeholder="Ej: 45"
            ),

            html.Div(
                "Es necesario completar todos los campos para poder realizar el estudio.",
                id="mensaje-aviso-1", 
                className="mensaje-aviso", 
                style={"display": "none"}
            ),
        ]),

        # Bloque hábitos
        html.Div(id="bloque-habitos", className="formulario-bloque", style={"display": "none"}, children=[
            html.Label("Consumo de alcohol (0 no / 1 sí)"),
            dcc.Dropdown(
                id="alcohol", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Label("Fruta diaria (0 no / 1 sí)"),
            dcc.Dropdown(
                id="fruta", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Label("Vegetales verdes (0 no / 1 sí)"),
            dcc.Dropdown(
                id="verduras", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Label("Papas fritas (0 no / 1 sí)"),
            dcc.Dropdown(
                id="papas", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Div(
                "Es necesario completar todos los campos para poder continuar.",
                id="mensaje-aviso-2", 
                className="mensaje-aviso", 
                style={"display": "none"}
            ),
        ]),

        # Bloque médico
        html.Div(id="bloque-medico", className="formulario-bloque", style={"display": "none"}, children=[
            html.Label("Salud general (1-5)"),
            dcc.Slider(
                id="salud_general", 
                min=1, 
                max=5, 
                step=1, 
                marks={i: str(i) for i in range(1, 6)},
                value=3
            ),

            html.Label("Chequeo médico reciente (0 no / 1 sí)"),
            dcc.Dropdown(
                id="chequeo", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Label("Ejercicio (0 no / 1 sí)"),
            dcc.Dropdown(
                id="ejercicio", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Label("Cáncer de piel (0 no / 1 sí)"),
            dcc.Dropdown(
                id="piel", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Label("Otro cáncer (0 no / 1 sí)"),
            dcc.Dropdown(
                id="cancer", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Label("Depresión (0 no / 1 sí)"),
            dcc.Dropdown(
                id="depresion", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Label("Diabetes (0 no / 1 sí)"),
            dcc.Dropdown(
                id="diabetes", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),

            html.Label("Artritis (0 no / 1 sí)"),
            dcc.Dropdown(
                id="artritis", 
                options=[{"label": str(i), "value": i} for i in [0, 1]],
                placeholder="Selecciona una opción"
            ),
            
            html.Label("Historial de tabaquismo"),
            dcc.Dropdown(
                id="smoking_history",
                options=[
                    {"label": "No fumador", "value": 0},
                    {"label": "Ex-fumador", "value": 1},
                    {"label": "Fumador actual", "value": 2}
                ],
                placeholder="Selecciona una opción"
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
    
    # Convertir edad a rango primero
    rango_edad = convertir_rango_edad(edad)
    if not rango_edad:
        return html.Div("Edad inválida. Debe ser un número entre 18 y 120"), ""
    
    campos = [altura, peso, imc, sexo, rango_edad, alcohol, fruta, verduras, papas,
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
            "edad": rango_edad,
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

if __name__ == "__main__":
    app.run(debug=True, port=8050)