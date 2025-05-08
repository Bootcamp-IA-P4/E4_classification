from fastapi import APIRouter, HTTPException
from models.schemas import PredictionInput, PredictionOutput
from services.model_service import make_prediction
from core.logging_config import setup_logger

router = APIRouter(prefix="/predict", tags=["predictions"])
logger = setup_logger(__name__)

@router.post("/", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    logger.info("📥 Recibida nueva solicitud de predicción")
    try:
        result = await make_prediction(input_data)
        logger.info("✅ Predicción completada exitosamente")
        return result
    except ValueError as e:
        logger.error(f"❌ Error de validación: {str(e)}", exc_info=True)
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error interno en el servidor: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error procesando la solicitud"
        )