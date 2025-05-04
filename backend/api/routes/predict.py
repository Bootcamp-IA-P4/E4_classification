from fastapi import APIRouter, HTTPException
from backend.services.model_service import make_prediction
from backend.models.schemas import PredictionInput, PredictionOutput

router = APIRouter(prefix="/predict", tags=["v1"])

@router.post("/", response_model=PredictionOutput)
async def predict_v1(input_data: PredictionInput):
    """Endpoint para predicciones (v1)"""
    try:
        return await make_prediction(input_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
