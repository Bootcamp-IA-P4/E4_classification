import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base  # Añade declarative_base
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
DB_DRIVER = "pymysql"

# Define Base aquí mismo
Base = declarative_base()

class DatabaseConfig:
    _instance = None
    # Patrón Singleton
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            self.initialized = True
            # Cargar variables de entorno
            env_path = Path(__file__).parent.parent.parent / '.env'
            if env_path.exists():
                load_dotenv(env_path)
            
            self.DB_USER = os.getenv("MYSQL_USER", "jdomdev")
            self.DB_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", ""))
            # Debug
            # print(f"Contraseña cargada: {self.DB_PASSWORD}")
            self.DB_HOST = os.getenv("MYSQL_HOST", "localhost")
            self.DB_NAME = os.getenv("MYSQL_DB", "heart_disease_db")
            self.DB_PORT = os.getenv("MYSQL_PORT", "3306")
            
            self.DB_DRIVER = "pymysql"  # Cambia a "mysqldb" o "mysqlconnector" según lo instalado
            
            self.DATABASE_URL = (
                f"mysql+{DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
            
            self.engine = None
            self.SessionLocal = None
    
    def initialize(self):
        if not hasattr(self, 'SessionLocal') or self.SessionLocal is None:
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

# Inicialización automática al importar el módulo
db_config = DatabaseConfig()
db_config.initialize()

# Asegúrate de exportar Base
__all__ = ['Base', 'db_config']

# Debug
print("\n=== Verificación de inicialización de la DB ===")
print(f"¿SessionLocal existe?: {hasattr(db_config, 'SessionLocal')}")
print(f"¿SessionLocal es callable?: {callable(getattr(db_config, 'SessionLocal', None))}")
print(f"Engine configurado: {db_config.engine is not None}\n")