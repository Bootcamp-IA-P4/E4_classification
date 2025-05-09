import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Configuración inicial de logging
def setup_logging(base_path: Path, app_folder: str):
    """Configura el sistema de logging"""
    logs_dir = base_path / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    log_file = logs_dir / f"setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

def create_back_structure(base_path: str = ".", app_folder: str = "backend"):
    """Crea la estructura del backend con logging mejorado"""
    base_path = Path(base_path)
    logger = setup_logging(base_path, app_folder)
    
    try:
        logger.info("🚀 Iniciando creación de estructura del backend...")
        
        paths = [
            f"{app_folder}/api/routes",
            f"{app_folder}/core",
            f"{app_folder}/data",
            f"{app_folder}/services",
            f"{app_folder}/static",
            f"{app_folder}/templates",
            f"{app_folder}/models",
            "logs"  # Carpeta para los logs
        ]

        # Crear directorios
        for path in paths:
            full_path = base_path / path
            os.makedirs(full_path, exist_ok=True)
            if app_folder in path and "api" not in path:  # Evitar __init__.py en routes
                (full_path / "__init__.py").touch()
            logger.info(f"📂 Carpeta creada: {full_path}")

        create_backend_files(base_path, app_folder, logger)
        
        logger.info(f"✅ Estructura backend creada en: {base_path / app_folder}")
        print(f"\n🎉 ¡Backend listo! Ver logs en: {base_path / 'logs'}")

    except Exception as e:
        logger.error(f"❌ Error crítico: {str(e)}", exc_info=True)
        raise

def create_backend_files(base_path: Path, app_folder: str, logger):
    """Crea los archivos principales con logging"""
    # 1. main.py
    main_content = f"""\
from fastapi import FastAPI
from {app_folder}.api.routes.predict import router as predict_router
from {app_folder}.core.config import settings
from {app_folder}.core.terminal_interface import TerminalInterface
import joblib
from pathlib import Path

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(predict_router, prefix="/api/v1")

# Ruta exacta del modelo (ajustado a tu nombre real)
MODEL_PATH = Path(__file__).parent / "data" / "modelo_predictor_enfermedad_cardiaca.pkl"

def run_terminal_interface():
    \"\"\"Ejecuta la interfaz de terminal\"\"\"
    model = joblib.load(MODEL_PATH)
    terminal = TerminalInterface(model)
    terminal.run()

if __name__ == "__main__":
    run_terminal_interface()
"""
    (base_path / f"{app_folder}/main.py").write_text(main_content)
    logger.info("📄 Archivo creado: main.py")

    # 2. config.py (con nombre exacto del modelo)
    config_content = f"""\
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "CVD Prediction API"
    API_V1_STR: str = "/api/v1"
    MODEL_PATH: str = "data/modelo_predictor_enfermedad_cardiaca.pkl"  # Nombre exacto
    FEATURES_PATH: str = "data/features_description.json"
    
    class Config:
        case_sensitive = True

settings = Settings()
"""
    (base_path / f"{app_folder}/core/config.py").write_text(config_content)
    logger.info("📄 Archivo creado: core/config.py")

    # 3. predict.py (con versionado v1)
    predict_content = f"""\
from fastapi import APIRouter, HTTPException
from {app_folder}.services.model_service import make_prediction
from {app_folder}.models.schemas import PredictionInput, PredictionOutput

router = APIRouter(prefix="/predict", tags=["v1"])

@router.post("/", response_model=PredictionOutput)
async def predict_v1(input_data: PredictionInput):
    \"\"\"Endpoint para predicciones (v1)\"\"\"
    try:
        return await make_prediction(input_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
"""
    (base_path / f"{app_folder}/api/routes/predict.py").write_text(predict_content)
    logger.info("📄 Archivo creado: api/routes/predict.py (v1)")

    # 4. model_service.py (con logging integrado)
    model_service_content = f"""\
import joblib
import pandas as pd
from pathlib import Path
from {app_folder}.core.config import settings
from {app_folder}.models.schemas import PredictionInput
import json
import logging

logger = logging.getLogger(__name__)

async def make_prediction(input_data: PredictionInput):
    \"\"\"Realiza predicciones con logging\"\"\"
    try:
        logger.info("🔮 Iniciando predicción...")
        model_path = Path(__file__).parent.parent.parent / settings.MODEL_PATH
        logger.debug(f"Cargando modelo desde: {{model_path}}")
        
        model = joblib.load(model_path)
        input_dict = input_data.dict()
        
        with open(Path(__file__).parent.parent.parent / settings.FEATURES_PATH) as f:
            features_def = json.load(f)["features"]
        
        # Validación de datos
        validated_data = {{}}
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
        logger.info(f"📊 Predicción completada. Probabilidad: {{proba:.2%}}")
        
        return {{
            "prediction": int(proba > 0.5),
            "probability": float(proba),
            "features_used": list(df.columns)
        }}
    except Exception as e:
        logger.error(f"❌ Error en predicción: {{str(e)}}", exc_info=True)
        raise
"""
    (base_path / f"{app_folder}/services/model_service.py").write_text(model_service_content)
    logger.info("📄 Archivo creado: services/model_service.py")

    # 5. features_description.json (igual que antes)
    features_data = {
        "features": {
            # ... (tus features existentes)
        },
        "translations": {
            # ... (tus traducciones existentes)
        }
    }
    features_path = base_path / f"{app_folder}/data/features_description.json"
    features_path.write_text(json.dumps(features_data, indent=2, ensure_ascii=False), encoding='utf-8')
    logger.info(f"📄 Archivo creado: data/features_description.json")

    # 6. Script de instalación (mejorado)
    install_script = """\
#!/bin/bash
# Instalación inteligente con uv
echo "⚙️ Configurando entorno virtual..."
python -m venv .venv-proj6
source .venv-proj6/bin/activate

install_package() {
    echo "📦 Instalando $1..."
    if uv add "$1"; then
        echo "✅ $1 instalado con uv add"
    else
        echo "⚠️ Falló uv add, intentando con pip..."
        pip install "$1"
    fi
}

packages=(
    "fastapi>=0.68.0"
    "uvicorn>=0.15.0"
    "pydantic>=1.8.0"
    "scikit-learn>=1.0.0"
    "pandas>=1.3.0"
    "joblib>=1.0.0"
    "python-multipart"
)

for pkg in "${packages[@]}"; do
    install_package "$pkg"
done

echo "🎉 Todas las dependencias instaladas"
"""
    (base_path / "install_dependencies.sh").write_text(install_script)
    os.chmod(base_path / "install_dependencies.sh", 0o755)
    logger.info("📄 Script creado: install_dependencies.sh")

if __name__ == "__main__":
    print("""
    🏗️  Constructor de Estructura Backend
    -----------------------------------
    """)
    target_folder = input("📍 ¿Dónde crear la estructura? (deja vacío para ./): ") or "."
    backend_name = input("🏷️  ¿Nombre de la carpeta backend? (predeterminado: 'backend'): ") or "backend"
    create_back_structure(target_folder, backend_name)