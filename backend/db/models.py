from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from db.database import Base

class PredictionRecord(Base):
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
    created_at = Column(DateTime(timezone=True), server_default=func.now())