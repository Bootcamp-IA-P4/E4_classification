from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

DB_USER = "root"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_NAME = "registros_usuarios"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)