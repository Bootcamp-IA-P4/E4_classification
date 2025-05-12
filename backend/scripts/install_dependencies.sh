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
