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
    salud_general = Column(String(50))
    chequeo_medico = Column(String(50))
    ejercicio = Column(String(50))
    cancer_piel = Column(String(50))
    otro_cancer = Column(String(50))
    depresion = Column(String(50))
    diabetes = Column(String(50))
    artritis = Column(String(50))
    sexo = Column(String(50))
    historial_tabaquismo = Column(String(50))
    edad = Column(String(50))
    resultado = Column(Integer)
    probabilidad = Column(Float)