from fastapi import FastAPI
from backend.api.routes.predict import router as predict_router
from backend.core.config import settings
from backend.core.terminal_interface import TerminalInterface
import joblib
from pathlib import Path

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(predict_router, prefix="/api/v1")

# Ruta exacta del modelo (ajustado a tu nombre real)
MODEL_PATH = Path(__file__).parent / "data" / "modelo_predictor_enfermedad_cardiaca.pkl"

def run_terminal_interface():
    """Ejecuta la interfaz de terminal"""
    model = joblib.load(MODEL_PATH)
    terminal = TerminalInterface(model)
    terminal.run()

if __name__ == "__main__":
    run_terminal_interface()
