import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from urllib.parse import quote_plus
from pathlib import Path
from dotenv import load_dotenv
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

Base = declarative_base()

class DatabaseConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            self.initialized = True
            self._load_config()
    
    def _load_config(self):
        """Carga la configuración desde variables de entorno"""
        env_path = Path(__file__).parent.parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        
        self.DB_USER = os.getenv("MYSQL_USER", "root")
        self.DB_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", "rootpassword"))
        self.DB_HOST = os.getenv("MYSQL_HOST", "db")
        self.DB_NAME = os.getenv("MYSQL_DB", "heart_disease_db")
        self.DB_PORT = os.getenv("MYSQL_PORT", "3306")
        self.DB_DRIVER = "pymysql"
        
        self.DATABASE_URL = (
            f"mysql+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        logger.info(f"Database URL: {self.DATABASE_URL.replace(self.DB_PASSWORD, '*****')}")
        
        self.engine = None
        self.session_factory = None
    
    def initialize(self):
        """Establece la conexión a la base de datos"""
        if not hasattr(self, 'session_factory') or self.session_factory is None:
            try:
                self._create_database_if_not_exists()
                self._setup_main_connection()
                logger.info(f"✅ Base de datos '{self.DB_NAME}' inicializada en {self.DB_HOST}")
                return True
            except Exception as e:
                logger.error(f"❌ Error de conexión: {str(e)}", exc_info=True)
                raise
    
    def _create_database_if_not_exists(self):
        """Crea la base de datos si no existe"""
        temp_url = (
            f"mysql+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
        )
        
        temp_engine = create_engine(temp_url, pool_pre_ping=True)
        
        with temp_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {self.DB_NAME}"))
            conn.execute(text(f"USE {self.DB_NAME}"))
            conn.commit()
    
    def _setup_main_connection(self):
        """Configura la conexión principal"""
        self.engine = create_engine(
            self.DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        self.session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    @contextmanager
    def get_session(self):
        """Proporciona una sesión gestionada automáticamente"""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

# Instancia global (ahora mejor gestionada)
db_config = DatabaseConfig()
db_config.initialize()

__all__ = ['Base', 'db_config', 'DatabaseConfig', 'PredictionRepository']