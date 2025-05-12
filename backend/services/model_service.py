from typing import Protocol, runtime_checkable
import joblib
import pandas as pd
from pathlib import Path
from models.schemas import PredictionInput, PredictionOutput
from core.config import settings
from db.repositories import PredictionRepository
from utils.mapping import MAPEO_ES_EN, MAPEO_EN_BDD
from core.logging_config import setup_logger

logger = setup_logger(__name__)

# --- Abstracciones para el principio Liskov ---
@runtime_checkable
class IModelLoader(Protocol):
    def load_model(self, model_path: str):
        ...
    
    def load_model_info(self, info_path: str):
        ...

@runtime_checkable
class IPredictionEngine(Protocol):
    def preprocess_data(self, input_data: dict) -> pd.DataFrame:
        ...
    
    def predict(self, df: pd.DataFrame) -> tuple[float, int]:
        ...

# --- Implementaciones concretas ---
class CardiacModelLoader(IModelLoader):
    def load_model(self, model_path: str):
        return joblib.load(model_path)
    
    def load_model_info(self, info_path: str):
        return joblib.load(info_path)

class LDAPredictionEngine(IPredictionEngine):
    def __init__(self, model_loader: IModelLoader):
        self.model = model_loader.load_model(settings.get_model_path())
        model_info = model_loader.load_model_info(settings.get_model_info_path())
        self.umbral_optimo = model_info["umbral_optimo"]
        self.variables_modelo = model_info["variables"]
        self.expected_columns = [
            "Height_(cm)", "Weight_(kg)", "BMI", "Alcohol_Consumption",
            # ... (resto de columnas)
        ]
    
    def preprocess_data(self, input_data: dict) -> pd.DataFrame:
        df = pd.DataFrame([input_data])
        df = df[self.expected_columns]
        
        # One-hot encoding
        if "age_category" in df.columns:
            df_age_cat = pd.get_dummies(df["age_category"], prefix="Age_Category")
            df = df.drop(["age_category"], axis=1)
            df = pd.concat([df, df_age_cat], axis=1)
        
        # Asegurar features requeridas
        for col in self.variables_modelo:
            if col not in df.columns:
                df[col] = 0
                
        return df[self.variables_modelo]
    
    def predict(self, df: pd.DataFrame) -> tuple[float, int]:
        proba = self.model.predict_proba(df)[:, 1][0]
        prediction = int(proba > self.umbral_optimo)
        
        # Ajuste visual
        if 0.3 <= proba <= 0.5:
            proba = 0.51
            
        return proba, prediction

# --- Servicio Principal ---
class PredictionService:
    def __init__(
        self,
        prediction_engine: IPredictionEngine,
        repository: PredictionRepository
    ):
        self.engine = prediction_engine
        self.repository = repository
    
    async def make_prediction(self, input_data: PredictionInput) -> PredictionOutput:
        try:
            logger.info("🔮 Iniciando predicción de riesgo cardiovascular...")
            
            # 1. Convertir datos
            english_data = input_data.to_english_dict()
            
            # 2. Preprocesamiento y predicción
            df = self.engine.preprocess_data(english_data)
            proba, prediction = self.engine.predict(df)
            
            logger.info(f"Probabilidad: {proba}, Predicción: {prediction}")
            
            # 3. Guardar en BD
            db_data = {
                MAPEO_EN_BDD[k]: v 
                for k, v in english_data.items()
                if k in MAPEO_EN_BDD
            }
            db_data.update({
                "prediction_result": prediction,
                "probability": float(proba)
            })
            
            self.repository.save_prediction(db_data)
            
            # 4. Retornar resultado
            return PredictionOutput(
                prediction=prediction,
                probability=float(proba),
                message="Riesgo cardiovascular alto" if prediction == 1 else "Riesgo bajo"
            )
            
        except Exception as e:
            logger.error(f"❌ Error en make_prediction: {str(e)}", exc_info=True)
            raise

# --- Factory para inyección de dependencias ---
def get_prediction_service() -> PredictionService:
    model_loader = CardiacModelLoader()
    prediction_engine = LDAPredictionEngine(model_loader)
    
    from db.database import db_config
    with db_config.get_session() as session:
        repository = PredictionRepository(session)
        return PredictionService(prediction_engine, repository)