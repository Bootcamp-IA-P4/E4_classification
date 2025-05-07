from sqlalchemy.orm import Session
from db.models import PredictionRecord
from db.database import db_config
import logging

logger = logging.getLogger(__name__)

def save_prediction_record(prediction_data: dict):
    try:
        db = db_config.SessionLocal()
        record = PredictionRecord(**prediction_data)
        db.add(record)
        db.commit()
        logger.info(f"Predicción guardada en DB con ID: {record.id}")
        return record
    except Exception as e:
        db.rollback()
        logger.error(f"Error al guardar predicción: {str(e)}")
        raise
    finally:
        db.close()