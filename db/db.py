from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base
from dotenv import load_dotenv
import os

load_dotenv()
print(f"DB_USER: {os.getenv('MYSQL_USER')}")
print(f"DB_PASSWORD: {os.getenv('MYSQL_PASSWORD')}")
print(f"DB_HOST: {os.getenv('MYSQL_HOST')}")
print(f"DB_NAME: {os.getenv('MYSQL_DB')}")
print(f"DB_PORT: {os.getenv('MYSQL_PORT')}")

DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_NAME = os.getenv("MYSQL_DB")
DB_PORT = os.getenv("MYSQL_PORT")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"DATABASE_URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)