import os
import json
from pathlib import Path

def create_project_structure(base_path: str = "cvd_backend"):
    """Crea la estructura completa del proyecto"""
    # Estructura principal
    paths = [
        # Backend
        "backend/app/api/routes",
        "backend/app/core",
        "backend/app/data",
        "backend/app/services",
        "backend/app/static",
        "backend/app/templates",
        
        # Frontend
        "frontend/dash_app/assets",
        "frontend/react_app/src"
    ]

    # Crear directorios
    for path in paths:
        os.makedirs(os.path.join(base_path, path), exist_ok=True)
        # Crear __init__.py solo en directorios Python
        if "app" in path or "services" in path or "core" in path or "routes" in path:
            Path(os.path.join(base_path, path, "__init__.py")).touch()

    # Archivos backend
    create_backend_files(base_path)
    
    # Archivos frontend (placeholders)
    Path(os.path.join(base_path, "frontend/dash_app/app.py")).touch()
    Path(os.path.join(base_path, "frontend/react_app/package.json")).touch()

    print(f"Estructura creada en: {os.path.abspath(base_path)}")

def create_backend_files(base_path: str):
    """Crea los archivos principales del backend"""
    backend_path = os.path.join(base_path, "backend")
    
    # 1. main.py
    main_py_content = """\
from fastapi import FastAPI
from app.api.routes.predict import router as predict_router
from app.core.config import settings
from app.core.terminal_interface import TerminalInterface
import joblib
from pathlib import Path

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(predict_router, prefix="/api/v1")

# Cargar modelo para terminal
MODEL_PATH = Path(__file__).parent / "data" / "modelo_predictor.pkl"

def run_terminal_interface():
    \"\"\"Ejecuta la interfaz de terminal\"\"\"
    model = joblib.load(MODEL_PATH)
    terminal = TerminalInterface(model)
    terminal.run()

if __name__ == "__main__":
    run_terminal_interface()
"""
    with open(os.path.join(backend_path, "app/main.py"), "w") as f:
        f.write(main_py_content)

    # 2. config.py
    config_py_content = """\
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CVD Prediction API"
    API_V1_STR: str = "/api/v1"
    MODEL_PATH: str = "data/modelo_predictor.pkl"
    FEATURES_PATH: str = "data/features_description.json"
    
    class Config:
        case_sensitive = True

settings = Settings()
"""
    with open(os.path.join(backend_path, "app/core/config.py"), "w") as f:
        f.write(config_py_content)

    # 3. predict.py (routes)
    predict_py_content = """\
from fastapi import APIRouter, HTTPException
from app.services.model_service import make_prediction
from app.models.schemas import PredictionInput, PredictionOutput

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    try:
        return await make_prediction(input_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
"""
    with open(os.path.join(backend_path, "app/api/routes/predict.py"), "w") as f:
        f.write(predict_py_content)

    # 4. model_service.py
    model_service_py_content = """\
import joblib
import pandas as pd
from pathlib import Path
from app.core.config import settings
from app.models.schemas import PredictionInput

async def make_prediction(input_data: PredictionInput):
    \"\"\"Realiza predicciones usando el modelo cargado\"\"\"
    # Cargar modelo
    model = joblib.load(Path(__file__).parent.parent.parent / settings.MODEL_PATH)
    
    # Convertir input a DataFrame
    input_dict = input_data.dict()
    df = pd.DataFrame([input_dict])
    
    # Asegurar columnas (para modelos sklearn)
    if hasattr(model, 'feature_names_in_'):
        missing_cols = set(model.feature_names_in_) - set(df.columns)
        for col in missing_cols:
            df[col] = 0  # Valor por defecto
        df = df[model.feature_names_in_]
    
    # Realizar predicción
    proba = model.predict_proba(df)[:, 1][0]
    
    return {
        "prediction": int(proba > 0.5),
        "probability": float(proba),
        "features_used": list(df.columns)
    }
"""
    with open(os.path.join(backend_path, "app/services/model_service.py"), "w") as f:
        f.write(model_service_py_content)

    # 5. terminal_interface.py
    terminal_py_content = """\
import pandas as pd
from app.services.translation_service import get_feature_translations, get_feature_descriptions
from app.models.schemas import PredictionInput

class TerminalInterface:
    def __init__(self, model):
        self.model = model
        self.translations = get_feature_translations()
        self.descriptions = get_feature_descriptions()

    def collect_input(self):
        \"\"\"Recolecta datos del usuario por terminal\"\"\"
        print("\\n=== Evaluación de Riesgo Cardiovascular ===")
        print("Complete la siguiente información (deje vacío para valores por defecto):\\n")
        
        user_data = {}
        for feature in self.model.feature_names_in_:
            esp_name = self.translations.get(feature, feature)
            desc = self.descriptions.get(feature, {}).get('description', '')
            default = self.descriptions.get(feature, {}).get('default', 0)
            
            print(f"{esp_name} ({desc})")
            value = input(f"[Valor por defecto: {default}]: ") or default
            user_data[feature] = float(value) if value.replace('.', '', 1).isdigit() else value
        
        return PredictionInput(**user_data)

    def run(self):
        \"\"\"Ejecuta la interfaz interactiva\"\"\"
        from app.services.model_service import make_prediction
        
        user_input = self.collect_input()
        result = await make_prediction(user_input)
        
        print("\\n=== Resultado ===")
        print(f"Riesgo: {'ALTO' if result['prediction'] else 'BAJO'}")
        print(f"Probabilidad: {result['probability']:.1%}")
        print("\\nRecomendación: Consulte a un especialista" if result['prediction'] 
              else "\\nRecomendación: Continúe con sus chequeos regulares")
"""
    with open(os.path.join(backend_path, "app/core/terminal_interface.py"), "w") as f:
        f.write(terminal_py_content)

    # 6. schemas.py
    schemas_py_content = """\
from pydantic import BaseModel
from typing import Dict, Optional
from app.services.translation_service import get_feature_descriptions

# Generar modelo dinámico basado en features
feature_descriptions = get_feature_descriptions()
fields = {name: (float, ... if desc.get('required', True) else (Optional[float], None))
           for name, desc in feature_descriptions.items()}

PredictionInput = type('PredictionInput', (BaseModel,), {
    '__annotations__': fields
})

class PredictionOutput(BaseModel):
    prediction: int
    probability: float
    features_used: list
"""
    with open(os.path.join(backend_path, "app/models/schemas.py"), "w") as f:
        f.write(schemas_py_content)

    # 7. translation_service.py
    translation_py_content = """\
import json
from pathlib import Path
from app.core.config import settings

def load_features_data():
    \"\"\"Carga el archivo JSON con las definiciones de features\"\"\"
    with open(Path(__file__).parent.parent.parent / settings.FEATURES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_feature_translations():
    \"\"\"Obtiene el diccionario de traducciones\"\"\"
    return load_features_data().get('translations', {})

def get_feature_descriptions():
    \"\"\"Obtiene las descripciones y metadatos de las features\"\"\"
    return load_features_data().get('features', {})
"""
    with open(os.path.join(backend_path, "app/services/translation_service.py"), "w") as f:
        f.write(translation_py_content)

    # 8. features_description.json
    features_json_content = {
        "features": {
            "age": {
                "description": "Edad del paciente en años",
                "type": "float",
                "range": [18, 100],
                "required": True,
                "default": 30
            },
            "sex": {
                "description": "Sexo biológico (0: Femenino, 1: Masculino)",
                "type": "int",
                "values": {
                    "0": "Femenino",
                    "1": "Masculino"
                },
                "required": True,
                "default": 0
            },
            "diabetes": {
                "description": "Diagnóstico de diabetes (0: No, 1: Sí)",
                "type": "int",
                "values": {
                    "0": "No",
                    "1": "Sí"
                },
                "required": True,
                "default": 0
            }
        },
        "translations": {
            "age": "Edad",
            "sex": "Sexo",
            "diabetes": "Diabetes"
        }
    }
    with open(os.path.join(backend_path, "app/data/features_description.json"), "w", encoding='utf-8') as f:
        json.dump(features_json_content, f, indent=2, ensure_ascii=False)

    # 9. requirements.txt
    requirements_content = """\
fastapi>=0.68.0
uvicorn>=0.15.0
pydantic>=1.8.0
scikit-learn>=1.0.0
pandas>=1.3.0
joblib>=1.0.0
python-multipart
"""
    with open(os.path.join(backend_path, "requirements.txt"), "w") as f:
        f.write(requirements_content)

    # 10. __init__.py files
    init_files = [
        "backend/app/__init__.py",
        "backend/app/api/__init__.py",
        "backend/app/models/__init__.py",
        "backend/app/services/__init__.py",
        "backend/app/core/__init__.py",
        "backend/app/api/routes/__init__.py"
    ]
    
    for init_file in init_files:
        with open(os.path.join(base_path, init_file), "w") as f:
            f.write('"""Package initialization"""\n')

if __name__ == "__main__":
    project_name = input("Nombre de la carpeta backend (deja vacío para 'cvd_backend'): ") or "cvd_backend"
    create_project_structure(project_name)