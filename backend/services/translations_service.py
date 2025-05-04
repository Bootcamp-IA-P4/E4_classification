import json
from pathlib import Path
from core.config import settings

def get_feature_translations():
    """Obtiene traducciones de features desde el JSON"""
    with open(Path(__file__).parent.parent / settings.FEATURES_PATH) as f:
        return json.load(f).get('translations', {})

def get_feature_descriptions():
    """Obtiene descripciones de features desde el JSON"""
    with open(Path(__file__).parent.parent / settings.FEATURES_PATH) as f:
        return json.load(f).get('features', {})