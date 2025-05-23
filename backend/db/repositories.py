from sqlalchemy.orm import Session
from db.models import PredictionRecord
from core.logging_config import setup_logger

logger = setup_logger(__name__)

class PredictionRepository:
    def __init__(self, db: Session):
        self.db = db
    def save_prediction(self, data: dict):
        try:
            logger.info("💾 Guardando predicción en base de datos...")
            
            # Verificar campos requeridos
            required_fields = [
    "height",
    "weight",
    "bmi",
    "alcohol_consumption",
    "fruit_consumption",
    "green_vegetables_consumption",
    "fried_potato_consumption",
    "general_health",
    "checkup",
    "exercise",
    "skin_cancer",
    "other_cancer",
    "depression",
    "diabetes",
    "arthritis",
    "sex",
    "smoking_history",
    "age_category",
    "prediction_result",
    "probability"
]
  # Añade todos los requeridos
            for field in required_fields:
                if field not in data or data[field] is None:
                    raise ValueError(f"Campo requerido faltante: {field}")
            
            # Crear el registro con solo los campos válidos
            valid_data = {
                k: v for k, v in data.items() 
                if hasattr(PredictionRecord, k)
            }
            
            registro = PredictionRecord(**valid_data)
            self.db.add(registro)
            self.db.commit()
            logger.info("✅ Predicción guardada exitosamente")
            return registro
        except Exception as e:
            self.db.rollback()
            logger.error(f"❌ Error al guardar en BD: {str(e)}", exc_info=True)
            raise
    
    def get_predictions(self, limit: int = 100):
        """Obtiene las últimas predicciones"""
        return self.db.query(PredictionRecord).order_by(PredictionRecord.id.desc()).limit(limit).all()

# Opcional: Interfaz abstracta para cumplir con DIP
from abc import ABC, abstractmethod

class IPredictionRepository(ABC):
    @abstractmethod
    def save_prediction(self, data: dict) -> PredictionRecord:
        pass
    
    @abstractmethod
    def get_predictions(self, limit: int):
        pass