#!/bin/bash

# Script de administración para la API de Ecommerce - UNTDF
# Solo para uso interno del administrador

echo "🔧 Script de Administración - API Ecommerce UNTDF"
echo "=================================================="
echo ""

# Cargar variables de entorno
if [ ! -f ".env" ]; then
    echo "❌ Error: Archivo .env no encontrado"
    echo "   Copia .env.example como .env y configura ADMIN_TOKEN"
    exit 1
fi

source .env

if [ -z "$ADMIN_TOKEN" ]; then
    echo "❌ Error: ADMIN_TOKEN no está configurado en .env"
    exit 1
fi

echo "🔑 Token de administrador encontrado"
echo ""

# Menú de opciones
echo "Selecciona una opción:"
echo "1. 🧹 Limpiar todo el sistema (PELIGROSO)"
echo "2. 🌱 Cargar datos de prueba"
echo "3. 📊 Ver estadísticas del sistema"
echo "4. 🚪 Salir"
echo ""

read -p "Opción (1-4): " option

case $option in
    1)
        echo ""
        echo "⚠️  ADVERTENCIA: Esto eliminará TODOS los datos y archivos del sistema"
        read -p "¿Estás seguro? (escribe 'CONFIRMAR' para continuar): " confirm
        
        if [ "$confirm" = "CONFIRMAR" ]; then
            echo "🧹 Ejecutando limpieza completa..."
            curl -X POST "http://localhost:8000/clean" \
                 -H "Authorization: Bearer $ADMIN_TOKEN" \
                 -H "Content-Type: application/json" | python3 -m json.tool
        else
            echo "❌ Operación cancelada"
        fi
        ;;
    2)
        echo ""
        echo "🌱 Cargando datos de prueba con token temporal..."
        curl -X POST "http://localhost:8000/seed" \
             -H "Authorization: Bearer admin_test_data" \
             -H "Content-Type: application/json" | python3 -m json.tool
        ;;
    3)
        echo ""
        echo "📊 Estadísticas del sistema:"
        echo "Productos:"
        curl -s -X GET "http://localhost:8000/products/" \
             -H "Authorization: Bearer admin_test_data" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'  Total: {len(data)} productos')"
        
        echo "Categorías:"
        curl -s -X GET "http://localhost:8000/categories/" \
             -H "Authorization: Bearer admin_test_data" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'  Total: {len(data)} categorías')"
        
        echo "Etiquetas:"
        curl -s -X GET "http://localhost:8000/tags/" \
             -H "Authorization: Bearer admin_test_data" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'  Total: {len(data)} etiquetas')"
        ;;
    4)
        echo "👋 ¡Hasta luego!"
        exit 0
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac
