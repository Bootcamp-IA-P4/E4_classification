from sqlalchemy.orm import Session
from db.models import PredictionRecord
from db.database import db_config
import logging

logger = logging.getLogger(__name__)

def save_prediction_record(prediction_data: dict):
    """Guarda los datos de la predicción en la base de datos"""
    try:
        db = db_config.SessionLocal()
        
        record = PredictionRecord(
            height=prediction_data.get("Height_(cm)"),
            weight=prediction_data.get("Weight_(kg)"),
            bmi=prediction_data.get("BMI"),
            general_health=prediction_data.get("General_Health"),
            age_category=prediction_data.get("Age_Category"),
            alcohol_consumption=prediction_data.get("Alcohol_Consumption"),
            fruit_consumption=prediction_data.get("Fruit_Consumption"),
            green_vegetables_consumption=prediction_data.get("Green_Vegetables_Consumption"),
            fried_potato_consumption=prediction_data.get("FriedPotato_Consumption"),
            checkup=prediction_data.get("Checkup"),
            exercise=prediction_data.get("Exercise"),
            skin_cancer=prediction_data.get("Skin_Cancer"),
            other_cancer=prediction_data.get("Other_Cancer"),
            depression=prediction_data.get("Depression"),
            diabetes=prediction_data.get("Diabetes"),
            arthritis=prediction_data.get("Arthritis"),
            sex=prediction_data.get("Sex"),
            smoking_history=prediction_data.get("Smoking_History"),
            prediction_result=prediction_data.get("prediction"),
            probability=prediction_data.get("probability")
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        logger.info(f"📝 Predicción guardada en DB con ID: {record.id}")
        return record
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al guardar predicción en DB: {str(e)}")
        raise
    finally:
        db.close()