#!/bin/bash

# Script para iniciar el servidor de desarrollo de la API de Ecommerce
# Universidad Nacional de Tierra del Fuego

echo "🚀 Iniciando servidor de API Ecommerce - UNTDF"
echo "📍 Puerto: 8000"
echo "📚 Documentación: http://localhost:8000/docs"
echo "🔗 API: http://localhost:8000"
echo "🌱 Seed endpoint: POST /seed (carga datos de prueba)"
echo ""

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    echo "📦 Activando entorno virtual..."
    source .venv/bin/activate
fi

# Instalar dependencias si no están instaladas
if [ ! -f ".venv/pyvenv.cfg" ] || [ ! -d ".venv/lib" ]; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Crear directorio de uploads si no existe
mkdir -p uploads

# Iniciar servidor
echo "🔥 Iniciando servidor con recarga automática..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
