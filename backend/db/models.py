from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class PredictionRecord(Base):
    """Modelo SQLAlchemy para almacenar predicciones"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    bmi = Column(Float, nullable=False)
    general_health = Column(Integer, nullable=False)
    age_category = Column(String(10), nullable=False)
    alcohol_consumption = Column(Float, nullable=False)
    fruit_consumption = Column(Float, nullable=False)
    green_vegetables_consumption = Column(Float, nullable=False)
    fried_potato_consumption = Column(Float, nullable=False)
    checkup = Column(Integer, nullable=False)
    exercise = Column(Integer, nullable=False)
    skin_cancer = Column(Integer, nullable=False)
    other_cancer = Column(Integer, nullable=False)
    depression = Column(Integer, nullable=False)
    diabetes = Column(Integer, nullable=False)
    arthritis = Column(Integer, nullable=False)
    sex = Column(Integer, nullable=False)
    smoking_history = Column(Integer, nullable=False)
    prediction_result = Column(Integer, nullable=False)
    probability = Column(Float, nullable=False)
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, result={self.prediction_result})>"