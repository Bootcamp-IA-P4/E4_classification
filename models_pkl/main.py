from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
import joblib
import numpy as np
import uvicorn

# Cargar modelo preentrenado
try:
    modelo = joblib.load("modelo_predictor_enfermedad_cardiaca.pkl")
except FileNotFoundError:
    print("Error: El archivo del modelo 'modelo_predictor_enfermedad_cardiaca.pkl' no se encontró.")
    modelo = None  # Manejar el caso en que el modelo no se carga

# Inicializar FastAPI
app = FastAPI(
    title="Predicción de Riesgo Cardiaco",
    description="API para predecir riesgo cardíaco (0: No riesgo, 1: Riesgo) usando un modelo ML",
    version="1.1"  # Incrementé la versión ya que hay cambios
)

# Clase para validar los datos de entrada
class DatosPaciente(BaseModel):
    edad: int = Field(..., ge=0, description="Edad del paciente en años")
    sexo: int = Field(..., ge=0, le=1, description="Sexo del paciente (0: Masculino, 1: Femenino)")
    altura: float = Field(..., gt=0, description="Altura del paciente en cm")
    peso: float = Field(..., gt=0, description="Peso del paciente en kg")
    imc: float = Field(..., description="Índice de Masa Corporal del paciente")
    alcohol: int = Field(..., ge=0, le=1, description="Consumo de alcohol (0: No, 1: Sí)")
    frutas: int = Field(..., ge=0, le=1, description="Consume frutas diariamente (0: No, 1: Sí)")
    vegetales: int = Field(..., ge=0, le=1, description="Consume vegetales verdes diariamente (0: No, 1: Sí)")
    fritos: int = Field(..., ge=0, le=1, description="Consume papas fritas (0: No, 1: Sí)")
    salud_general: int = Field(..., ge=1, le=5, description="Salud general del paciente (1: Excelente, 5: Pobre)")
    chequeo: int = Field(..., ge=0, le=1, description="Chequeo médico reciente (0: No, 1: Sí)")
    ejercicio: int = Field(..., ge=0, le=1, description="Realiza ejercicio regularmente (0: No, 1: Sí)")
    cancer_piel: int = Field(..., ge=0, le=1, description="Historial de cáncer de piel (0: No, 1: Sí)")
    otro_cancer: int = Field(..., ge=0, le=1, description="Historial de otro tipo de cáncer (0: No, 1: Sí)")
    depresion: int = Field(..., ge=0, le=1, description="Sufre o ha sufrido depresión (0: No, 1: Sí)")
    diabetes: int = Field(..., ge=0, le=1, description="Tiene diabetes (0: No, 1: Sí)")
    artritis: int = Field(..., ge=0, le=1, description="Tiene artritis (0: No, 1: Sí)")

# Ya que la predicción es binaria, la función de clasificación de riesgo no es necesaria.
# Vamos a interpretar directamente la predicción del modelo.

@app.post("/predecir")
async def predecir_riesgo(datos: DatosPaciente):
    if modelo is None:
        return {"error": "El modelo no se ha cargado correctamente."}
    try:
        entrada = np.array([[
            datos.edad,
            datos.sexo,
            datos.altura,
            datos.peso,
            datos.imc,
            datos.alcohol,
            datos.frutas,
            datos.vegetales,
            datos.fritos,
            datos.salud_general,
            datos.chequeo,
            datos.ejercicio,
            datos.cancer_piel,
            datos.otro_cancer,
            datos.depresion,
            datos.diabetes,
            datos.artritis
        ]])

        prediccion = modelo.predict(entrada)[0]

        riesgo_texto = "Sí" if prediccion == 1 else "No"
        mensaje = "Recomendamos una consulta médica." if prediccion == 1 else "Riesgo bajo o inexistente."

        return {
            "riesgo_prediccion": int(prediccion),  # Devolvemos la predicción como entero (0 o 1)
            "riesgo_texto": riesgo_texto,
            "mensaje": mensaje
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)