#!/usr/bin/env python3
"""
Script de ejemplo para probar la API de Ecommerce
Universidad Nacional de Tierra del Fuego
"""

import requests
import json

BASE_URL = "http://localhost:8000"
TOKEN = "estudiante_demo_123"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_api():
    print("🧪 Probando API de Ecommerce - UNTDF")
    print("=" * 50)
    
    try:
        # Test root endpoint
        print("1. Probando endpoint raíz...")
        response = requests.get(BASE_URL)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        print()
        
        # Test create category
        print("2. Creando categoría...")
        category_data = {
            "title": "Electrónicos",
            "description": "Productos electrónicos y tecnología"
        }
        response = requests.post(f"{BASE_URL}/categories/", 
                               json=category_data, headers=HEADERS)
        print(f"   ✅ Status: {response.status_code}")
        category = response.json()
        print(f"   📄 Categoría creada: {category}")
        category_id = category["id"]
        print()
        
        # Test create tag
        print("3. Creando etiqueta...")
        tag_data = {"title": "Nuevo"}
        response = requests.post(f"{BASE_URL}/tags/", 
                               json=tag_data, headers=HEADERS)
        print(f"   ✅ Status: {response.status_code}")
        tag = response.json()
        print(f"   📄 Etiqueta creada: {tag}")
        tag_id = tag["id"]
        print()
        
        # Test create product
        print("4. Creando producto...")
        product_data = {
            "title": "iPhone 15",
            "description": "Smartphone Apple último modelo",
            "price": 999.99,
            "category_id": category_id,
            "tag_ids": [tag_id]
        }
        response = requests.post(f"{BASE_URL}/products/", 
                               json=product_data, headers=HEADERS)
        print(f"   ✅ Status: {response.status_code}")
        product = response.json()
        print(f"   📄 Producto creado: {product}")
        product_id = product["id"]
        print()
        
        # Test list products
        print("5. Listando productos...")
        response = requests.get(f"{BASE_URL}/products/", headers=HEADERS)
        print(f"   ✅ Status: {response.status_code}")
        products = response.json()
        print(f"   📄 Productos encontrados: {len(products)}")
        print()
        
        # Test get specific product
        print("6. Obteniendo producto específico...")
        response = requests.get(f"{BASE_URL}/products/{product_id}", headers=HEADERS)
        print(f"   ✅ Status: {response.status_code}")
        product_detail = response.json()
        print(f"   📄 Producto: {product_detail['title']} - ${product_detail['price']}")
        print()
        
        print("🎉 ¡Todas las pruebas completadas exitosamente!")
        print("🔗 Visita http://localhost:8000/docs para más información")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
        print("   Ejecuta: ./start.sh o uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_api()
