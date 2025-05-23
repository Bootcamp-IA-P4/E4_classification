from pydantic import BaseModel, Field
from typing import Literal, Optional
from enum import Enum

# Enums para mejor validación
class GeneralHealthOptions(int, Enum):
    EXCELENTE = 5
    MUY_BUENA = 4
    BUENA = 3
    REGULAR = 2
    MALA = 1

class DiabetesOptions(int, Enum):
    NO = 0
    PRE = 1
    SI = 2
    EMBARAZO = 3

AgeCategoryOptions = Literal[
    "18-24", "25-29", "30-34", "35-39", "40-44", "45-49",
    "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"
]

class PredictionInput(BaseModel):
    """Esquema para datos de entrada en español"""
    altura: float = Field(..., gt=0, description="Altura en cm")
    peso: float = Field(..., gt=0, description="Peso en kg")
    imc: float = Field(..., gt=0, le=100, description="Índice de masa corporal")
    salud_general: GeneralHealthOptions
    consumo_alcohol: float = Field(..., ge=0, description="Consumo semanal de alcohol")
    consumo_fruta: float = Field(..., ge=0, description="Consumo diario de fruta")
    consumo_vegetales: float = Field(..., ge=0, description="Consumo diario de vegetales")
    consumo_papas: float = Field(..., ge=0, description="Consumo semanal de papas fritas")
    chequeo_medico: int = Field(..., ge=0, le=4, description="Frecuencia de chequeos médicos")
    ejercicio: int = Field(..., ge=0, le=1, description="Realiza ejercicio (0=No, 1=Sí)")
    cancer_piel: int = Field(..., ge=0, le=1, description="Historial de cáncer de piel")
    otro_cancer: int = Field(..., ge=0, le=1, description="Historial de otros cánceres")
    depresion: int = Field(..., ge=0, le=1, description="Diagnóstico de depresión")
    diabetes: DiabetesOptions
    artritis: int = Field(..., ge=0, le=1, description="Diagnóstico de artritis")
    sexo: int = Field(..., ge=0, le=1, description="Sexo (0=Masculino, 1=Femenino)")
    historial_tabaquismo: int = Field(..., ge=0, le=1, description="Historial de tabaquismo")
    edad: AgeCategoryOptions

    class Config:
        allow_population_by_field_name = True  # permite model_dump con names
    
    def to_english_dict(self):
        """Convierte los nombres a inglés para el modelo"""
        from utils.mapping import MAPEO_ES_EN  # Import local para evitar circular imports
        return {
            MAPEO_ES_EN[k]: v for k, v in self.model_dump().items()
            if k in MAPEO_ES_EN  # Solo incluye campos mapeados
        }

class PredictionOutput(BaseModel):
    """Esquema para la respuesta de predicción"""
    risk_level: Literal["high", "low"]
    probability: float = Field(..., ge=0, le=1, description="Probabilidad entre 0 y 1")
    message: Optional[str] = Field(
        None, 
        description="Mensaje descriptivo del resultado"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "risk_level": "high",
                "probability": 0.87,
                "message": "Riesgo cardiovascular alto"
            }
        }