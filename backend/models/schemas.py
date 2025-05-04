from pydantic import BaseModel
from typing import Dict, Literal, Union

# Tipos para categorías
GeneralHealthOptions = Literal[1, 2, 3, 4, 5]
AgeCategoryOptions = Literal[
    "18-24", "25-29", "30-34", "35-39", "40-44", "45-49",
    "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"
]

class PredictionInput(BaseModel):
    """Esquema para datos de entrada basado en features_description.json"""
    Height_cm: float  # Nota: Puedes usar Height_(cm) si cambias Field(alias="Height_(cm)")
    Weight_kg: float
    BMI: float
    General_Health: GeneralHealthOptions
    Age_Category: AgeCategoryOptions
    Alcohol_Consumption: float
    Fruit_Consumption: float
    Green_Vegetables_Consumption: float
    FriedPotato_Consumption: float
    Checkup: int
    Exercise: int
    Skin_Cancer: int
    Other_Cancer: int
    Depression: int
    Diabetes: int
    Arthritis: int
    Sex: int
    Smoking_History: int

    class Config:
        schema_extra = {
            "example": {
                "Height_cm": 170,
                "Weight_kg": 70,
                "BMI": 24.2,
                "General_Health": 3,
                "Age_Category": "35-39",
                # ... otros campos con valores por defecto
            }
        }

class PredictionOutput(BaseModel):
    """Respuesta de la API"""
    prediction: Literal[0, 1]  # 0: No riesgo, 1: Riesgo
    probability: float  # Valor entre 0 y 1
    features_used: list[str]
    message: str  # Mensaje descriptivo

    class Config:
        schema_extra = {
            "example": {
                "prediction": 1,
                "probability": 0.87,
                "features_used": ["Height_cm", "Weight_kg", ...],
                "message": "Riesgo cardiovascular alto"
            }
        }