from contextlib import asynccontextmanager
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.terminal_interface import TerminalInterface
import joblib
from pathlib import Path
import sys
from core.logging_config import setup_logger
from db.database import db_config
from db.models import Base
# Configuración de rutas API
from api.v1.routes.predict import router as predict_router

# Configuración básica de logging
logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Iniciando aplicación FastAPI...")
    try:
        # Inicializar base de datos
        db_config.initialize()
        Base.metadata.create_all(bind=db_config.engine)
        logger.info("✅ Base de datos inicializada correctamente")
        
        # Cargar modelo
        global model
        MODEL_PATH = Path(__file__).parent / settings.MODEL_PATH
        model = joblib.load(MODEL_PATH)
        logger.info(f"✅ Modelo cargado desde: {MODEL_PATH}")
        
        yield  # Application runs here

    except Exception as e:
        logger.error(f"❌ Error durante el startup: {str(e)}")
        raise
    
    # Shutdown
    logger.info("🛑 Cerrando aplicación FastAPI...")

# Crea UNA sola instancia de FastAPI con lifespan
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.include_router(predict_router, prefix=settings.API_V1_STR)
# Configuración CORS (justo después de crear la app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8050"],  # En producción, reemplazar con ["https://tudominio.com"]
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

def run_terminal_interface():
    """Ejecuta la interfaz de terminal"""
    try:
        terminal = TerminalInterface(model)
        terminal.run()
    except Exception as e:
        logger.error(f"❌ Error en la interfaz de terminal: {str(e)}")
        raise
    try:
        terminal = TerminalInterface(model)
        terminal.run()
    except Exception as e:
        logger.error(f"❌ Error en la interfaz de terminal: {str(e)}")
        raise

if __name__ == "__main__":
    if "--terminal" in sys.argv or "-t" in sys.argv:
        run_terminal_interface()
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")