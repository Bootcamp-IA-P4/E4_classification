import joblib
import pandas as pd
from pathlib import Path
import json
import logging
from models.schemas import PredictionInput
from core.config import settings
from .database_service import save_prediction_record
from utils.mapping import MAPEO_ES_EN, MAPEO_EN_BDD
from core.logging_config import setup_logger

logger = setup_logger(__name__)

async def make_prediction(input_data: PredictionInput):
    try:
        logger.info("🔮 Iniciando predicción de riesgo cardiovascular...")

        # 1. Cargar modelo y parámetros
        model = joblib.load(settings.get_model_path())
        logger.debug(f"✅ Modelo cargado desde: {settings.get_model_path()}")
        info_modelo = joblib.load(settings.get_model_info_path())
        # info_modelo = joblib.load(Path(settings.get_model_path()).parent / "info_modelo_cardiaco.pkl")
        umbral_optimo = info_modelo["umbral_optimo"]
        variables_modelo = info_modelo["variables"]

        # 2. Convertir datos a inglés
        english_data = input_data.to_english_dict()
        
        # 3. Preparar DataFrame para predicción
        df = pd.DataFrame([english_data])
        logger.info(f"DataFrame creado con columnas: {df.columns.tolist()}")
        
        # Asegurar que las columnas están en el orden correcto
        expected_columns = [
            "Height_(cm)", "Weight_(kg)", "BMI", "Alcohol_Consumption",
            "Fruit_Consumption", "Green_Vegetables_Consumption", "FriedPotato_Consumption",
            "General_Health", "Checkup", "Exercise", "Skin_Cancer", "Other_Cancer",
            "Depression", "Diabetes", "Arthritis", "Sex", "Smoking_History", "Age_Category"
        ]
        
        # Reordenar las columnas si es necesario
        df = df[expected_columns]
        logger.debug(f"DataFrame reordenado: {df.columns.tolist()}")

        # One-hot encoding para Age_Category
        if "age_category" in df.columns:
            df_age_cat = pd.get_dummies(df["age_category"], prefix="Age_Category")
            df = df.drop(["age_category"], axis=1)
            df = pd.concat([df, df_age_cat], axis=1)

        # Asegurar todas las features requeridas
        for col in variables_modelo:
            if col not in df.columns:
                df[col] = 0
        df = df[variables_modelo]

        # 4. Realizar predicción
        proba = model.predict_proba(df)[:, 1][0]
        logger.info(f"Probabilidad raw: {proba}")

        # Ajuste visual
        proba_mostrar = proba
        if 0.3 <= proba <= 0.5:
            proba_mostrar = 0.51
            logger.debug(f"Probabilidad ajustada: {proba_mostrar}")
        
        prediction = int(proba > umbral_optimo)
        logger.info(f"Predicción final: {prediction}")

        # 5. Guardar en BD (con nombres de columnas BD)
        db_data = {
            MAPEO_EN_BDD[k]: v 
            for k, v in english_data.items()
            if k in MAPEO_EN_BDD
        }
        db_data.update({
            "prediction_result": prediction,
            "probability": float(proba_mostrar)
        })
        save_prediction_record(db_data)

        from models.schemas import PredictionOutput

        return PredictionOutput(
            prediction=prediction,
            probability=float(proba_mostrar),
            message="Riesgo cardiovascular alto" if prediction == 1 else "Riesgo bajo"
        )

    except Exception as e:
        logger.error(f"Error en make_prediction: {str(e)}", exc_info=True)
        raise