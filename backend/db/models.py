from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import logging
# from backend.db.database import Base

logger = logging.getLogger(__name__)

Base = declarative_base()

class PredictionRecord(Base):
    """Modelo SQLAlchemy para almacenar predicciones"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    height_cm = Column("Height_(cm)", Float, nullable=False)  # Altura en cm
    weight_kg = Column("Weight_(kg)", Float, nullable=False)  # Peso en kg
    bmi = Column("BMI", Float, nullable=False)  # Índice de masa corporal
    general_health = Column("General_Health", Integer, nullable=False)  # 1-5
    age_category = Column("Age_Category", String(10), nullable=False)  # Ej: "18-24"
    alcohol_consumption = Column("Alcohol_Consumption", Float, nullable=False)
    fruit_consumption = Column("Fruit_Consumption", Float, nullable=False)
    green_vegetables_consumption = Column("Green_Vegetables_Consumption", Float, nullable=False)
    fried_potato_consumption = Column("FriedPotato_Consumption", Float, nullable=False)
    checkup = Column("Checkup", Integer, nullable=False)  # 0-4
    exercise = Column("Exercise", Integer, nullable=False)  # 0-1
    skin_cancer = Column("Skin_Cancer", Integer, nullable=False)  # 0-1
    other_cancer = Column("Other_Cancer", Integer, nullable=False)  # 0-1
    depression = Column("Depression", Integer, nullable=False)  # 0-1
    diabetes = Column("Diabetes", Integer, nullable=False)  # 0-1
    arthritis = Column("Arthritis", Integer, nullable=False)  # 0-1
    sex = Column("Sex", Integer, nullable=False)  # 0-1
    smoking_history = Column("Smoking_History", Integer, nullable=False)  # 0-2
    heart_disease_prediction = Column(Integer, nullable=False)  # 0-1
    probability = Column(Float, nullable=False)  # 0.0-1.0
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, result={self.prediction_result})>"