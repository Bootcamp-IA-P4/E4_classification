# test_model_unit.py
import os
import joblib
import numpy as np
import pytest
from pathlib import Path
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1] 
MODELS_PATH = PROJECT_ROOT / 'backend' / 'data'
MODEL_FILE = MODELS_PATH / "modelo_predictor_enfermedad_cardiaca.pkl"
INFO_FILE = MODELS_PATH / "info_modelo_cardiaco.pkl"
SCALER_FILE = MODELS_PATH / "scaler_modelo_cardiaco.pkl"

@pytest.mark.unit
@pytest.mark.parametrize("file_path", [MODEL_FILE, INFO_FILE])
def test_pkl_files_exist(file_path):
    assert os.path.exists(file_path), f"El archivo {file_path} no existe."

@pytest.mark.unit
def test_model_load():
    modelo = joblib.load(MODEL_FILE)
    assert hasattr(modelo, 'predict'), "El modelo no tiene método predict."
    assert hasattr(modelo, 'predict_proba'), "El modelo no tiene método predict_proba."

@pytest.mark.unit
def test_info_modelo_keys():
    info = joblib.load(INFO_FILE)
    assert 'umbral_optimo' in info
    assert 'variables' in info
    assert 'traduccion' in info

@pytest.mark.unit
def test_predict_shape():
    import pandas as pd
    modelo = joblib.load(MODEL_FILE)
    info = joblib.load(INFO_FILE)
    # Crear un DataFrame con los nombres de las variables
    X = pd.DataFrame(
        np.zeros((1, len(info['variables']))),
        columns=info['variables']
    )
    y_pred = modelo.predict(X)
    y_proba = modelo.predict_proba(X)
    assert y_pred.shape == (1,)
    assert y_proba.shape == (1, 2)

@pytest.mark.unit
def test_scaler_load_and_transform():
    if os.path.exists(SCALER_FILE):
        scaler = joblib.load(SCALER_FILE)
        arr = np.array([[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]])
        arr_scaled = scaler.transform(arr)
        assert arr_scaled.shape == arr.shape
    else:
        pytest.skip("No se encontró scaler_modelo_cardiaco.pkl, test omitido.")
