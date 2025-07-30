#!/usr/bin/env python3
"""
Script de prueba para el endpoint de limpieza (interno)
Universidad Nacional de Tierra del Fuego
"""

import requests
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

BASE_URL = "http://localhost:8000"

def test_clean_functionality():
    print("🧹 Probando funcionalidad de limpieza (INTERNO) - UNTDF")
    print("=" * 60)
    
    # Obtener token de administrador desde .env
    admin_token = os.getenv("ADMIN_TOKEN")
    if not admin_token:
        print("❌ Error: Variable ADMIN_TOKEN no encontrada en .env")
        return
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    try:
        # Paso 1: Cargar algunos datos de prueba primero
        print("1. Cargando datos de prueba con seed...")
        test_token = "test_clean_demo"
        test_headers = {"Authorization": f"Bearer {test_token}"}
        
        response = requests.post(f"{BASE_URL}/seed", headers=test_headers)
        if response.status_code == 200:
            seed_stats = response.json()["statistics"]
            print(f"   ✅ Datos cargados:")
            print(f"      - Productos: {seed_stats['products_created']}")
            print(f"      - Categorías: {seed_stats['categories_created']}")
            print(f"      - Etiquetas: {seed_stats['tags_created']}")
            print(f"      - Imágenes: {seed_stats['images_downloaded']}")
        else:
            print(f"   ❌ Error cargando seed: {response.text}")
            return
        print()
        
        # Paso 2: Verificar que los datos existen
        print("2. Verificando datos existentes...")
        response = requests.get(f"{BASE_URL}/products/", headers=test_headers)
        products_before = response.json()
        
        response = requests.get(f"{BASE_URL}/categories/", headers=test_headers)
        categories_before = response.json()
        
        response = requests.get(f"{BASE_URL}/tags/", headers=test_headers)
        tags_before = response.json()
        
        print(f"   📊 Productos antes: {len(products_before)}")
        print(f"   📊 Categorías antes: {len(categories_before)}")
        print(f"   📊 Etiquetas antes: {len(tags_before)}")
        print()
        
        # Paso 3: Ejecutar limpieza con token de admin
        print("3. Ejecutando limpieza completa...")
        response = requests.post(f"{BASE_URL}/clean", headers=headers)
        
        if response.status_code == 200:
            clean_result = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📄 Mensaje: {clean_result['message']}")
            print(f"   📊 Estadísticas de limpieza:")
            stats = clean_result['statistics']
            print(f"      - Productos eliminados: {stats['products_deleted']}")
            print(f"      - Categorías eliminadas: {stats['categories_deleted']}")
            print(f"      - Etiquetas eliminadas: {stats['tags_deleted']}")
            print(f"      - Archivos eliminados: {stats['files_deleted']}")
            print(f"      - Errores: {len(stats['errors'])}")
            if stats['errors']:
                print(f"      - Detalles: {stats['errors']}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            return
        print()
        
        # Paso 4: Verificar que los datos fueron eliminados
        print("4. Verificando que los datos fueron eliminados...")
        response = requests.get(f"{BASE_URL}/products/", headers=test_headers)
        products_after = response.json()
        
        response = requests.get(f"{BASE_URL}/categories/", headers=test_headers)
        categories_after = response.json()
        
        response = requests.get(f"{BASE_URL}/tags/", headers=test_headers)
        tags_after = response.json()
        
        print(f"   📊 Productos después: {len(products_after)}")
        print(f"   📊 Categorías después: {len(categories_after)}")
        print(f"   📊 Etiquetas después: {len(tags_after)}")
        print()
        
        # Paso 5: Probar con token incorrecto
        print("5. Probando seguridad con token incorrecto...")
        wrong_headers = {"Authorization": "Bearer token_incorrecto"}
        response = requests.post(f"{BASE_URL}/clean", headers=wrong_headers)
        
        if response.status_code == 403:
            print("   ✅ Seguridad funcionando: acceso denegado con token incorrecto")
        else:
            print(f"   ❌ Problema de seguridad: {response.status_code}")
        print()
        
        # Verificación final
        if (len(products_after) == 0 and len(categories_after) == 0 and 
            len(tags_after) == 0):
            print("🎉 ¡Limpieza completa exitosa!")
            print("✅ Todos los datos fueron eliminados correctamente")
            print("✅ Seguridad del endpoint funcionando")
            print("⚠️  Recordar: Este endpoint es solo para uso interno")
        else:
            print("❌ La limpieza no fue completa")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_clean_functionality()
