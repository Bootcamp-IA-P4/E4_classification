import joblib
import pandas as pd
from pathlib import Path
from backend.core.config import settings
from backend.models.schemas import PredictionInput
import json
import logging

logger = logging.getLogger(__name__)

async def make_prediction(input_data: PredictionInput):
    """Realiza predicciones con logging"""
    try:
        logger.info("🔮 Iniciando predicción...")
        model_path = Path(__file__).parent.parent.parent / settings.MODEL_PATH
        logger.debug(f"Cargando modelo desde: {model_path}")
        
        model = joblib.load(model_path)
        input_dict = input_data.dict()
        
        with open(Path(__file__).parent.parent.parent / settings.FEATURES_PATH) as f:
            features_def = json.load(f)["features"]
        
        # Validación de datos
        validated_data = {}
        for feature, value in input_dict.items():
            if feature in features_def:
                if features_def[feature]["type"] == "float":
                    validated_data[feature] = float(value)
                else:
                    validated_data[feature] = value
        
        df = pd.DataFrame([validated_data])
        
        if hasattr(model, 'feature_names_in_'):
            missing_cols = set(model.feature_names_in_) - set(df.columns)
            for col in missing_cols:
                df[col] = 0
            df = df[model.feature_names_in_]
        
        proba = model.predict_proba(df)[:, 1][0]
        logger.info(f"📊 Predicción completada. Probabilidad: {proba:.2%}")
        
        return {
            "prediction": int(proba > 0.5),
            "probability": float(proba),
            "features_used": list(df.columns)
        }
    except Exception as e:
        logger.error(f"❌ Error en predicción: {str(e)}", exc_info=True)
        raise
