from pathlib import Path
from pydantic_settings import BaseSettings
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    PROJECT_NAME: str = "CVD Prediction API"
    API_V1_STR: str = "/api/v1"
    
    # Rutas relativas al directorio del proyecto (backend/)
    MODEL_PATH: str = "data/modelo_predictor_enfermedad_cardiaca.pkl"
    FEATURES_PATH: str = "data/features_description.json"
    
    # Configuración de base de datos
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = "localhost"
    MYSQL_DB: str = "heart_disease_prediction"
    MYSQL_PORT: str = "3306"
    
    # Método para obtener paths absolutos
    def get_features_path(self):
        return Path(__file__).parent.parent / self.FEATURES_PATH
    
    def get_model_path(self):
        return Path(__file__).parent.parent / self.MODEL_PATH

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()