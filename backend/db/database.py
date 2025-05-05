import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
DB_DRIVER = "pymysql"

class DatabaseConfig:
    def __init__(self):
        # Cargar variables de entorno
        env_path = Path(__file__).parent.parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        
        self.DB_USER = os.getenv("MYSQL_USER", "jdomdev")
        self.DB_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", ""))
        print(f"Contraseña cargada: {self.DB_PASSWORD}")  # ← Debug
        self.DB_HOST = os.getenv("MYSQL_HOST", "localhost")
        self.DB_NAME = os.getenv("MYSQL_DB", "heart_disease_db")
        self.DB_PORT = os.getenv("MYSQL_PORT", "3306")
        
        # Elige UNO de estos drivers:
        self.DB_DRIVER = "pymysql"  # Cambia a "mysqldb" o "mysqlconnector" según lo instalado
        
        self.DATABASE_URL = (
            f"mysql+{DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        
        self.engine = None
        self.SessionLocal = None
    
    def initialize(self):
        try:
            # Conexión temporal sin especificar base de datos
            temp_url = (
                f"mysql+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/"
            )
            
            temp_engine = create_engine(temp_url, pool_pre_ping=True)
            
            with temp_engine.connect() as conn:
                conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.DB_NAME}"))
                conn.execute(text(f"USE {self.DB_NAME}"))
                conn.commit()
            
            # Conexión principal
            self.engine = create_engine(
                self.DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info(f"✅ Base de datos '{self.DB_NAME}' inicializada en {self.DB_HOST}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error de conexión: {str(e)}", exc_info=True)
            raise

db_config = DatabaseConfig()