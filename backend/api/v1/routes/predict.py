from fastapi import APIRouter, HTTPException, Depends
from models.schemas import PredictionInput, PredictionOutput
from core.logging_config import setup_logger
from db.database import db_config
from db.repositories import PredictionRepository
from typing import Protocol, runtime_checkable
from sqlalchemy.orm import Session

router = APIRouter(prefix="/predict", tags=["predictions"])
logger = setup_logger(__name__)

# --- Abstracción para el principio Liskov ---
@runtime_checkable
class IPredictionService(Protocol):
    async def predict(self, input_data: PredictionInput) -> PredictionOutput:
        ...

# Implementación concreta compatible con LSP
class LDAPredictionService:
    def __init__(self, model_repository: PredictionRepository):
        self.repository = model_repository
    
    async def predict(self, input_data: PredictionInput) -> PredictionOutput:
        """Implementación específica para modelo LDA"""
        logger.info("🔍 Procesando predicción con modelo LDA...")
        # Aquí iría tu lógica actual de make_prediction()
        prediction_data = {
            "probability": 0.85,  # Ejemplo
            "risk_level": "high"
        }
        
        # Guardar en BD (inyectado)
        self.repository.save_prediction(prediction_data)
        
        return PredictionOutput(
            risk_level=prediction_data["risk_level"],
            probability=prediction_data["probability"]
        )

# --- Dependencias ---
def get_db_session():
    """Generador de sesiones para inyección"""
    with db_config.get_session() as session:
        yield session

def get_prediction_service(
    db: Session = Depends(get_db_session)
) -> IPredictionService:
    """Inyección del servicio que cumple LSP"""
    return LDAPredictionService(
        model_repository=PredictionRepository(db)
    )

# --- Endpoint ---
@router.post("/", response_model=PredictionOutput)
async def predict(
    input_data: PredictionInput,
    prediction_service: IPredictionService = Depends(get_prediction_service)
):
    logger.info("📥 Recibida nueva solicitud de predicción")
    try:
        result = await prediction_service.predict(input_data)
        logger.info("✅ Predicción completada exitosamente")
        return result
    except ValueError as e:
        logger.error(f"❌ Error de validación: {str(e)}", exc_info=True)
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error interno: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error procesando la solicitud"
        )