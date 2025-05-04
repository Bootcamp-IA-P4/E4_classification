from fastapi import FastAPI
from core.config import settings
from core.terminal_interface import TerminalInterface
import joblib
from pathlib import Path
import sys

app = FastAPI(title=settings.PROJECT_NAME)

# Configuración de rutas API
from api.v1.routes.predict import router as predict_router
app.include_router(predict_router, prefix="/api/v1")

# Carga del modelo
MODEL_PATH = Path(__file__).parent / settings.MODEL_PATH
model = joblib.load(MODEL_PATH)

def run_terminal_interface():
    """Ejecuta la interfaz de terminal"""
    terminal = TerminalInterface(model)
    terminal.run()

if __name__ == "__main__":
    # Si se ejecuta con --terminal o -t, inicia la interfaz de consola
    if "--terminal" in sys.argv or "-t" in sys.argv:
        run_terminal_interface()
    else:
        # Inicia el servidor FastAPI normalmente
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)