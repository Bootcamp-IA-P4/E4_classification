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
from core.config import settings

class CardiacModelLoader(IModelLoader):
    def load_model(self, model_path: str = None):
        try:
            full_path = settings.get_model_path()
            logger.info(f"⏳ Cargando modelo desde: {full_path}")
            if not full_path.exists():
                raise FileNotFoundError(f"Archivo de modelo no encontrado en {full_path}")
            model = joblib.load(full_path)
            logger.info("✅ Modelo cargado correctamente")
            return model
        except Exception as e:
            logger.error(f"❌ Error cargando modelo: {str(e)}", exc_info=True)
            raise

    def load_model_info(self, info_path: str = None):
        try:
            full_path = settings.get_model_info_path()
            logger.info(f"⏳ Cargando metadatos del modelo desde: {full_path}")
            if not full_path.exists():
                raise FileNotFoundError(f"Archivo de metadatos no encontrado en {full_path}")
            info = joblib.load(full_path)
            required_keys = ["umbral_optimo", "variables"]
            if not all(key in info for key in required_keys):
                raise ValueError("El archivo de metadatos no tiene la estructura esperada")
            logger.info("✅ Metadatos del modelo cargados correctamente")
            return info
        except Exception as e:
            logger.error(f"❌ Error cargando metadatos: {str(e)}", exc_info=True)
            raise

class LDAPredictionEngine(IPredictionEngine):
    def __init__(self, model_loader: IModelLoader):
        self.model = model_loader.load_model()
        model_info = model_loader.load_model_info()

        self.umbral_optimo = model_info["umbral_optimo"]
        self.variables_modelo = model_info["variables"]
        self.mapeo_es_en = MAPEO_ES_EN

        # Columnas esperadas por el modelo
        self.expected_columns = self.variables_modelo

    def preprocess_data(self, input_data: dict) -> pd.DataFrame:
        # Convertir de español a nombres técnicos
        english_data = {
            self.mapeo_es_en.get(k, k): v
            for k, v in input_data.items()
        }

        df = pd.DataFrame([english_data])

        # Asegurar columnas esperadas
        for col in self.expected_columns:
            if col not in df.columns:
                df[col] = 0  # O valor por defecto
        return df[self.expected_columns]

    def predict(self, df: pd.DataFrame) -> tuple[float, int]:
        proba = self.model.predict_proba(df)[:, 1][0]
        prediction = int(proba > self.umbral_optimo)
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
        self.map_es_en = MAPEO_ES_EN
        self.map_en_bdd = MAPEO_EN_BDD

    async def make_prediction(self, input_data: PredictionInput) -> PredictionOutput:
        try:
            logger.info("🔮 Iniciando predicción de riesgo cardiovascular...")

            # 1. Convertir a nombres técnicos en inglés
            technical_data = {
                self.map_es_en[k]: v
                for k, v in input_data.model_dump().items()
                if k in self.map_es_en
            }

            logger.debug(f"📄 Datos técnicos en inglés: {technical_data}")

            # 2. Preprocesar y predecir
            df = self.engine.preprocess_data(technical_data)
            proba, prediction = self.engine.predict(df)

            logger.debug(f"📈 Resultado: proba={proba}, prediction={prediction}")

            # 3. Preparar datos para base de datos con nombres en BDD
            data_to_save = {
                self.map_en_bdd.get(k, k): v
                for k, v in technical_data.items()
            }

            data_to_save.update({
                "prediction_result": prediction,
                "probability": float(proba)
            })

            self.repository.save_prediction(data_to_save)

            # 4. Devolver respuesta al usuario
            return PredictionOutput(
                risk_level="high" if prediction == 1 else "low",
                probability=proba,
                message="Riesgo cardiovascular alto" if prediction == 1 else "Riesgo bajo"
            )
        except Exception as e:
            logger.error(f"❌ Error en make_prediction: {str(e)}", exc_info=True)
            raise

# --- Factory ---
def get_prediction_service() -> PredictionService:
    model_loader = CardiacModelLoader()
    prediction_engine = LDAPredictionEngine(model_loader)
    from db.database import db_config
    with db_config.get_session() as session:
        repository = PredictionRepository(session)
        return PredictionService(prediction_engine, repository)