from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CVD Prediction API"
    API_V1_STR: str = "/api/v1"
    MODEL_PATH: str = "data/modelo_predictor_enfermedad_cardiaca.pkl"  # Nombre exacto
    FEATURES_PATH: str = "data/features_description.json"
    
    class Config:
        case_sensitive = True

settings = Settings()
