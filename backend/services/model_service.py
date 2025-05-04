import joblib
import pandas as pd
from pathlib import Path
import json
import logging
from models.schemas import PredictionInput
from core.config import settings

logger = logging.getLogger(__name__)

async def make_prediction(input_data: PredictionInput):
    """Realiza predicciones con validación y logging mejorado"""
    try:
        logger.info("🔮 Iniciando predicción de riesgo cardiovascular...")
        
        # 1. Cargar modelo usando path desde settings
        model = joblib.load(settings.get_model_path())
        logger.debug(f"✅ Modelo cargado desde: {settings.get_model_path()}")
        
        # 2. Validar y procesar datos de entrada
        input_dict = input_data.model_dump()
        validated_data = {}
        
        with open(settings.get_features_path()) as f:
            features_def = json.load(f)["features"]
        logger.debug("✅ Definiciones de features cargadas")
        
        # Validación tipo/rango
        for feature, value in input_dict.items():
            if feature in features_def:
                feat_def = features_def[feature]
                
                # Validación para tipos numéricos
                if feat_def["type"] == "float":
                    try:
                        num_value = float(value)
                        if not (feat_def["range"][0] <= num_value <= feat_def["range"][1]):
                            raise ValueError(f"Valor {num_value} fuera de rango para {feature}")
                        validated_data[feature] = num_value
                    except ValueError as e:
                        logger.error(f"❌ Error validando {feature}: {str(e)}")
                        raise
                
                # Validación para categorías
                elif "values" in feat_def:
                    if str(value) not in feat_def["values"]:
                        valid_values = ", ".join(feat_def["values"].keys())
                        raise ValueError(f"Valor inválido para {feature}. Opciones: {valid_values}")
                    validated_data[feature] = value
                
                else:
                    validated_data[feature] = value

        # 3. Preparar DataFrame
        df = pd.DataFrame([validated_data])
        
        # Asegurar todas las features esperadas por el modelo
        if hasattr(model, 'feature_names_in_'):
            missing_cols = set(model.feature_names_in_) - set(df.columns)
            for col in missing_cols:
                df[col] = 0  # Valor por defecto para features faltantes
            df = df[model.feature_names_in_]  # Orden correcto
        
        # 4. Realizar predicción
        proba = model.predict_proba(df)[:, 1][0]
        prediction = int(proba > 0.5)  # Umbral de 0.5
        
        logger.info(f"📊 Resultado - Predicción: {prediction}, Probabilidad: {proba:.2%}")
        
        # 5. Generar respuesta
        return {
            "prediction": prediction,
            "probability": float(proba),
            "features_used": list(df.columns),
            "message": "Riesgo cardiovascular alto" if prediction == 1 else "Riesgo bajo"
        }

    except FileNotFoundError as e:
        logger.error(f"❌ Archivo no encontrado: {str(e)}")
        raise
    except json.JSONDecodeError:
        logger.error("❌ Error decodificando el archivo de features")
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado: {str(e)}", exc_info=True)
        raise