from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.models import Base
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()

DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD_RAW = os.getenv("MYSQL_PASSWORD")
DB_PASSWORD = quote_plus(DB_PASSWORD_RAW) if DB_PASSWORD_RAW else ''
DB_HOST = os.getenv("MYSQL_HOST")
DB_NAME = os.getenv("MYSQL_DB")
DB_PORT = os.getenv("MYSQL_PORT")

# Crear engine temporal para crear la base de datos si no existe
tmp_engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/")
try:
    with tmp_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.commit()
except Exception as e:
    print(f"Error creando la base de datos: {e}")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"DATABASE_URL: {DATABASE_URL}")
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"DATABASE_URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Verificación explícita de conexión
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("Conexión a la base de datos exitosa.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

def init_db():
    Base.metadata.create_all(bind=engine)