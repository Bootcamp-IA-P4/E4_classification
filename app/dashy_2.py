import dash
from dash import html, dcc, Input, Output, State, ctx
import requests
import dash_daq as daq

# Configuración
BACKEND_URL = "http://localhost:8050"
PREDICT_ENDPOINT = f"{BACKEND_URL}/predict/"

# App initialization
app = dash.Dash(
    __name__,
    assets_folder='assets',
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="Riesgo Cardiaco",
    update_title=None,
    suppress_callback_exceptions=True
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

# Estilos reutilizables
block_style = {
    "padding": "20px",
    "border": "1px solid #ddd",
    "borderRadius": "5px",
    "margin": "10px"
}

input_style = {
    "margin": "10px",
    "width": "200px"
}

# Layout completo
app.layout = html.Div([
    html.Div([
        html.H1("Evaluación de Riesgo Cardíaco", style={"textAlign": "center"}),
        html.Img(src="assets/heart.png", style={"height": "60px", "display": "block", "margin": "0 auto"})
    ], style={"textAlign": "center"}),
    
    # Bloque general
    html.Div([
        html.H2("Datos Generales"),
        dcc.Input(id="altura", type="number", placeholder="Altura (cm)", style=input_style),
        dcc.Input(id="peso", type="number", placeholder="Peso (kg)", style=input_style),
        dcc.Input(id="imc", type="number", placeholder="IMC", disabled=True, style=input_style),
        html.Div([
            html.Label("Sexo:", style={"marginRight": "10px"}),
            dcc.RadioItems(
                id="sexo",
                options=[
                    {"label": "Hombre", "value": 1},
                    {"label": "Mujer", "value": 0}
                ],
                inline=True,
                style={"margin": "10px"}
            )
        ]),
        dcc.Input(id="edad", type="number", placeholder="Edad", min=18, max=120, style=input_style),
        html.Div(
            id="mensaje-aviso-1",
            children="Complete todos los campos para continuar",
            style={"color": "red", "margin": "10px"}
        )
    ], id="bloque-general", style=block_style),
    
    # Bloque hábitos
    html.Div([
        html.H2("Hábitos de Vida"),
        html.Div([
            html.Label("Consumo de alcohol:"),
            dcc.RadioItems(
                id="alcohol",
                options=[
                    {"label": "No", "value": 0},
                    {"label": "Ocasional", "value": 1},
                    {"label": "Frecuente", "value": 2}
                ],
                inline=True,
                style={"margin": "10px"}
            )
        ]),
        
        html.Div([
            html.Label("Consumo de frutas al día:"),
            dcc.RadioItems(
                id="fruta",
                options=[
                    {"label": "Nada", "value": 0},
                    {"label": "1-2 porciones", "value": 1},
                    {"label": "3+ porciones", "value": 2}
                ],
                inline=True,
                style={"margin": "10px"}
            )
        ]),
        
        html.Div([
            html.Label("Consumo de verduras al día:"),
            dcc.RadioItems(
                id="verduras",
                options=[
                    {"label": "Nada", "value": 0},
                    {"label": "1-2 porciones", "value": 1},
                    {"label": "3+ porciones", "value": 2}
                ],
                inline=True,
                style={"margin": "10px"}
            )
        ]),
        
        html.Div([
            html.Label("Consumo de papas fritas/snacks:"),
            dcc.RadioItems(
                id="papas",
                options=[
                    {"label": "Nunca", "value": 0},
                    {"label": "Ocasional", "value": 1},
                    {"label": "Frecuente", "value": 2}
                ],
                inline=True,
                style={"margin": "10px"}
            )
        ]),
        
        html.Div(
            id="mensaje-aviso-2",
            children="Complete todos los campos para continuar",
            style={"color": "red", "margin": "10px"}
        )
    ], id="bloque-habitos", style={**block_style, "display": "none"}),
    
    # Bloque médico
    html.Div([
        html.H2("Historial Médico"),
        
        html.Div([
            html.Label("Estado de salud general:"),
            dcc.Slider(
                id="salud_general",
                min=1,
                max=5,
                marks={
                    1: "Muy pobre",
                    2: "Pobre",
                    3: "Regular",
                    4: "Buena",
                    5: "Excelente"
                },
                value=3,
                included=False
            )
        ], style={"margin": "20px"}),
        
        html.Div([
            html.Label("Último chequeo médico:"),
            dcc.RadioItems(
                id="chequeo",
                options=[
                    {"label": "Menos de 1 año", "value": 1},
                    {"label": "1-2 años", "value": 2},
                    {"label": "Más de 2 años", "value": 3},
                    {"label": "Nunca", "value": 4}
                ],
                inline=True,
                style={"margin": "10px"}
            )
        ]),
        
        html.Div([
            html.Label("Ejercicio físico semanal:"),
            dcc.RadioItems(
                id="ejercicio",
                options=[
                    {"label": "Nada", "value": 0},
                    {"label": "1-2 veces", "value": 1},
                    {"label": "3+ veces", "value": 2}
                ],
                inline=True,
                style={"margin": "10px"}
            )
        ]),
        
        html.Div([
            html.Label("Diagnósticos previos:"),
            daq.BooleanSwitch(id="piel", label="Cáncer de piel", on=False, style={"margin": "10px"}),
            daq.BooleanSwitch(id="cancer", label="Otro cáncer", on=False, style={"margin": "10px"}),
            daq.BooleanSwitch(id="depresion", label="Depresión", on=False, style={"margin": "10px"}),
            daq.BooleanSwitch(id="diabetes", label="Diabetes", on=False, style={"margin": "10px"}),
            daq.BooleanSwitch(id="artritis", label="Artritis", on=False, style={"margin": "10px"})
        ]),
        
        html.Button(
            "Evaluar Riesgo",
            id="submit-button",
            style={
                "margin": "20px",
                "padding": "10px 20px",
                "backgroundColor": "#007BFF",
                "color": "white",
                "border": "none",
                "borderRadius": "5px"
            }
        )
    ], id="bloque-medico", style={**block_style, "display": "none"}),
    
    # Área de resultados
    html.Div(id="resultado", style=block_style),
    html.Div(id="datos-para-enviar", style={"display": "none"})
])

# Callbacks (se mantienen igual que en tu versión original)
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
    State("piel", "on"),
    State("cancer", "on"),
    State("depresion", "on"),
    State("diabetes", "on"),
    State("artritis", "on"),
)
def mostrar_resultado(n_clicks, altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
                     salud_general, chequeo, ejercicio, piel, cancer, depresion, diabetes, artritis):
    if not n_clicks:
        return "", ""
    
    campos = [altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
              salud_general, chequeo, ejercicio]
    
    if any(x is None for x in campos):
        return html.Div("Por favor, completa todos los campos antes de evaluar.", style={"color": "red"}), ""

    datos = {
        "altura": altura,
        "peso": peso,
        "imc": imc,
        "sexo": sexo,
        "edad": str(edad),
        "consumo_alcohol": alcohol,
        "consumo_fruta": fruta,
        "consumo_vegetales": verduras,
        "consumo_papas": papas,
        "salud_general": salud_general,
        "chequeo_medico": chequeo,
        "ejercicio": ejercicio,
        "cancer_piel": 1 if piel else 0,
        "otro_cancer": 1 if cancer else 0,
        "depresion": 1 if depresion else 0,
        "diabetes": 1 if diabetes else 0,
        "artritis": 1 if artritis else 0,
        "historial_tabaquismo": 0
    }
    # Debug
    print(f"Línea 317(dash.py)")
    print("Datos enviados al backend:", datos)  # <-- Añade esto

    try:
        response = requests.post(
            PREDICT_ENDPOINT,
            json=datos,
            headers={"Content-Type": "application/json"}
        )
        # Debug
        print("Respuesta del backend:", response.text)  # <-- Añade esto
        response.raise_for_status()
        resultado = response.json()

        riesgo_color = "red" if resultado["prediction"] == 1 else "green"
        mensaje = ("⚠️ Riesgo elevado de enfermedad cardíaca. Consulte a su médico." 
                  if resultado["prediction"] == 1 
                  else "✅ Bajo riesgo de enfermedad cardíaca.")
        
        return html.Div([
            html.H2("Resultado de la evaluación:"),
            html.P(f"Probabilidad: {round(resultado['probability']*100)}%", 
                  style={"fontSize": "1.2em", "fontWeight": "bold"}),
            html.P(f"Riesgo: {'Alto' if resultado['prediction'] == 1 else 'Bajo'}", 
                  style={"color": riesgo_color, "fontSize": "1.5em", "fontWeight": "bold"}),
            html.P(mensaje, style={"fontSize": "1.2em"})
        ]), str(datos)

    except requests.exceptions.RequestException as e:
        return html.Div(f"Error al conectar con el servidor: {str(e)}", style={"color": "red"}), ""

if __name__ == "__main__":
    app.run(debug=True)