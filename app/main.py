from fastapi import FastAPI
from app.api.routes.predict import router as predict_router
from app.core.config import settings
from app.core.terminal_interface import TerminalInterface
import joblib
from pathlib import Path

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(predict_router, prefix="/api/v1")

MODEL_PATH = Path(__file__).parent / "data" / "modelo_predictor.pkl"

def run_terminal_interface():
    """Ejecuta la interfaz de terminal"""
    model = joblib.load(MODEL_PATH)
    terminal = TerminalInterface(model)
    terminal.run()

if __name__ == "__main__":
    run_terminal_interface()
