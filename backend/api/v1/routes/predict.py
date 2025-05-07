from fastapi import APIRouter, HTTPException
from models.schemas import PredictionInput, PredictionOutput
from services.model_service import make_prediction
import logging

router = APIRouter(prefix="/predict", tags=["predictions"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    
    try:
        logger.info("Solicitud de predicción recibida")
        logger.debug("Datos de entrada: %s", input_data.model_dump())
        
        result = await make_prediction(input_data)
        
        logger.info("Predicción completada exitosamente")
        return result
        
    except ValueError as e:
        logger.error("Error de validación: %s", str(e))
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error("Error interno: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error procesando la solicitud"
        )    