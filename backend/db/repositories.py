from sqlalchemy.orm import Session
from db.models import PredictionRecord
from core.logging_config import setup_logger

logger = setup_logger(__name__)

class PredictionRepository:
    """Implementa el patrón Repository para las predicciones"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save_prediction(self, data: dict) -> PredictionRecord:
        """Guarda una predicción en la base de datos"""
        try:
            logger.info("💾 Guardando predicción en base de datos...")
            registro = PredictionRecord(**data)
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