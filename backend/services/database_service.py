from sqlalchemy.orm import Session
from db.models import PredictionRecord
from db.database import db_config
from core.logging_config import setup_logger

logger = setup_logger(__name__)

def save_prediction_record(data: dict):
    try:
        logger.info("💾 Guardando predicción en base de datos...")
        db = db_config.SessionLocal()
        registro = PredictionRecord(**data)
        db.add(registro)
        db.commit()
        logger.info("✅ Predicción guardada exitosamente")
        return registro
    except Exception as e:
        logger.error(f"❌ Error al guardar en BD: {str(e)}", exc_info=True)
        raise
    finally:
        db.close()