import dash
from dash import html, dcc, Input, Output, State
import requests
import dash_daq as daq

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

# Helper function
def calcular_imc(peso, altura_cm):
    try:
        altura_m = altura_cm / 100
        return round(peso / (altura_m ** 2), 2)
    except:
        return None

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
)
def mostrar_resultado(n_clicks, altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
                     salud_general, chequeo, ejercicio, piel, cancer, depresion, diabetes, artritis):

    if not n_clicks:
        return "", ""
    campos = [altura, peso, imc, sexo, edad, alcohol, fruta, verduras, papas,
              salud_general, chequeo, ejercicio, piel, cancer, depresion, diabetes, artritis]
    if any(x is None for x in campos):
        return html.Div("Por favor, completa todos los campos antes de evaluar."), ""

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
        "Age": edad,
        "Smoking_History": 0  # Suponemos fijo
    }

    try:
        response = requests.post("http://localhost:8050/api/v1/routes/predict", json=datos)
        if response.status_code == 200:
            resultado = response.json()
            pred = resultado.get("prediccion", 0)
            riesgo = "ALTO" if pred == 1 else "BAJO"
            return html.Div(f"Riesgo Cardiovascular: {riesgo}", className="resultado-texto"), str(datos)
        else:
            return html.Div("Error al procesar los datos. Intente más tarde."), ""
    except Exception as e:
        return html.Div(f"Error de conexión con el backend: {str(e)}"), ""

if __name__ == '__main__':
    app.run(debug=True)

