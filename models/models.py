from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prediccion(Base):
    __tablename__ = 'registros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    altura = Column(Float)
    peso = Column(Float)
    imc = Column(Float)
    consumo_alcohol = Column(Integer)
    consumo_fruta = Column(Integer)
    consumo_vegetales = Column(Integer)
    consumo_papas = Column(Integer)
    salud_general = Column(Integer)
    chequeo_medico = Column(Integer)
    ejercicio = Column(Integer)
    cancer_piel = Column(Integer)
    otro_cancer = Column(Integer)
    depresion = Column(Integer)
    diabetes = Column(Integer)
    artritis = Column(Integer)
    sexo = Column(Integer)
    historial_tabaquismo = Column(Integer)
    edad = Column(String(50))
    resultado = Column(Integer)         
    probabilidad = Column(Float)        
