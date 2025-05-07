from pydantic import BaseModel
from typing import Literal
from utils.mapping import MAPEO_ES_EN

# Tipos para categorías
GeneralHealthOptions = Literal[1, 2, 3, 4, 5]
AgeCategoryOptions = Literal[
    "18-24", "25-29", "30-34", "35-39", "40-44", "45-49",
    "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"
]

class PredictionInput(BaseModel):
    """Esquema para datos de entrada en español"""
    altura: float
    peso: float
    imc: float
    salud_general: GeneralHealthOptions
    edad: AgeCategoryOptions
    consumo_alcohol: float
    consumo_fruta: float
    consumo_vegetales: float
    consumo_papas: float
    chequeo_medico: int
    ejercicio: int
    cancer_piel: int
    otro_cancer: int
    depresion: int
    diabetes: int
    artritis: int
    sexo: int
    historial_tabaquismo: int

    def to_english_dict(self):
        """Convierte los nombres a inglés para el modelo"""
        return {
            MAPEO_ES_EN[k]: v for k, v in self.model_dump().items()
        }

from pydantic import BaseModel

class PredictionOutput(BaseModel):
    """Esquema para la respuesta de predicción"""
    prediction: int  # 0 o 1
    probability: float
    message: str

    class Config:
        schema_extra = {
            "example": {
                "prediction": 1,
                "probability": 0.87,
                "message": "Riesgo cardiovascular alto"
            }
        }

