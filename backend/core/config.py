import os
from pathlib import Path
from pydantic import BaseSettings

import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    PROJECT_NAME: str = "CVD Prediction API"
    API_V1_STR: str = "/api/v1/routes"
    
    # Rutas relativas al directorio del proyecto (backend/)
    MODEL_PATH: str = "data/modelo_predictor_enfermedad_cardiaca.pkl"
    MODEL_INFO_PATH: str = "data/info_modelo_cardiaco.pkl"
    FEATURES_PATH: str = "data/features_description.json"
    
    # Configuración de base de datos
    MYSQL_USER: str = "jdomdev"
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = "localhost"
    MYSQL_DB: str = "heart_disease_db"
    MYSQL_PORT: str = "3306"
    
    # Método para obtener paths absolutos
    def get_features_path(self):
        return Path(__file__).parent.parent / self.FEATURES_PATH
    
    def get_model_path(self):
        return Path(__file__).parent.parent / self.MODEL_PATH
    def get_model_info_path(self):
        return Path(__file__).parent.parent / self.MODEL_INFO_PATH

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()