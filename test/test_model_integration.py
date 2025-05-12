# test_model_integration.py
import os
import joblib
import numpy as np
import pandas as pd
import pytest
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1] 
MODELS_PATH = PROJECT_ROOT / 'backend' / 'data'
MODEL_FILE = MODELS_PATH / "modelo_predictor_enfermedad_cardiaca.pkl"
INFO_FILE = MODELS_PATH / "info_modelo_cardiaco.pkl"
SCALER_FILE = MODELS_PATH / "scaler_modelo_cardiaco.pkl"

@pytest.fixture(scope="module")
def modelo_y_info():
    modelo = joblib.load(MODEL_FILE)
    info = joblib.load(INFO_FILE)
    scaler = joblib.load(SCALER_FILE) if os.path.exists(SCALER_FILE) else None
    return modelo, info, scaler

@pytest.mark.integration
def test_pipeline_predict(modelo_y_info):
    modelo, info, scaler = modelo_y_info
    # Simula datos de entrada válidos
    variables = info['variables']
    # Valores de ejemplo: todos ceros excepto una edad categórica
    X = pd.DataFrame([np.zeros(len(variables))], columns=variables)
    # Si hay columnas de edad categórica, pon una a 1
    edad_cols = [col for col in variables if col.startswith('Age_Category_')]
    if edad_cols:
        X[edad_cols[0]] = 1
    # Si tienes scaler, aplica a numéricas
    if scaler:
        num_cols = [col for col in variables if col in ['Height_(cm)','Weight_(kg)','BMI','Alcohol_Consumption','Fruit_Consumption','Green_Vegetables_Consumption','FriedPotato_Consumption']]
        if num_cols:
            X.loc[:, num_cols] = scaler.transform(X[num_cols])
    # Predicción
    proba = modelo.predict_proba(X)[:, 1][0]
    pred = modelo.predict(X)[0]
    assert 0.0 <= proba <= 1.0
    assert pred in [0, 1]

@pytest.mark.integration
def test_pipeline_with_realistic_input(modelo_y_info):
    modelo, info, scaler = modelo_y_info
    variables = info['variables']
    # Ejemplo de datos realistas
    data = {k: 0 for k in variables}
    for col in variables:
        if col.startswith('Age_Category_'):
            data[col] = 1
            break
    # Valores típicos para numéricas
    for col in ['Height_(cm)','Weight_(kg)','BMI']:
        if col in data:
            data[col] = 170 if col == 'Height_(cm)' else 70 if col == 'Weight_(kg)' else 24.0
    X = pd.DataFrame([data])
    if scaler:
        num_cols = [col for col in variables if col in ['Height_(cm)','Weight_(kg)','BMI','Alcohol_Consumption','Fruit_Consumption','Green_Vegetables_Consumption','FriedPotato_Consumption']]
        if num_cols:
            X.loc[:, num_cols] = scaler.transform(X[num_cols])
    proba = modelo.predict_proba(X)[:, 1][0]
    pred = modelo.predict(X)[0]
    assert 0.0 <= proba <= 1.0
    assert pred in [0, 1]
