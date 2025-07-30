#!/usr/bin/env python3
"""
Script de prueba específico para el endpoint de Seed
Universidad Nacional de Tierra del Fuego
"""

import requests
import json

BASE_URL = "http://localhost:8000"
TOKEN = "test_seed_demo_456"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_seed_functionality():
    print("🌱 Probando funcionalidad de Seed - UNTDF")
    print("=" * 60)
    
    try:
        # Test 1: Verificar que no hay datos inicialmente
        print("1. Verificando estado inicial...")
        response = requests.get(f"{BASE_URL}/products/", headers=HEADERS)
        initial_products = response.json()
        print(f"   📊 Productos iniciales: {len(initial_products)}")
        
        response = requests.get(f"{BASE_URL}/categories/", headers=HEADERS)
        initial_categories = response.json()
        print(f"   📊 Categorías iniciales: {len(initial_categories)}")
        
        response = requests.get(f"{BASE_URL}/tags/", headers=HEADERS)
        initial_tags = response.json()
        print(f"   📊 Etiquetas iniciales: {len(initial_tags)}")
        print()
        
        # Test 2: Ejecutar seed
        print("2. Ejecutando seed...")
        response = requests.post(f"{BASE_URL}/seed", headers=HEADERS)
        print(f"   ✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            seed_result = response.json()
            print(f"   📄 Mensaje: {seed_result['message']}")
            print(f"   📊 Estadísticas:")
            stats = seed_result['statistics']
            print(f"      - Categorías creadas: {stats['categories_created']}")
            print(f"      - Productos creados: {stats['products_created']}")
            print(f"      - Etiquetas creadas: {stats['tags_created']}")
            print(f"      - Imágenes descargadas: {stats['images_downloaded']}")
            print(f"      - Errores: {len(stats['errors'])}")
            if stats['errors']:
                print(f"      - Detalles de errores: {stats['errors']}")
        else:
            print(f"   ❌ Error: {response.text}")
            return
        print()
        
        # Test 3: Verificar datos después del seed
        print("3. Verificando datos cargados...")
        
        # Verificar productos
        response = requests.get(f"{BASE_URL}/products/", headers=HEADERS)
        products = response.json()
        print(f"   📊 Total productos: {len(products)}")
        
        # Mostrar algunos productos de ejemplo
        print("   📝 Ejemplos de productos:")
        for i, product in enumerate(products[:5]):
            tags_str = ", ".join([tag["title"] for tag in product["tags"]]) if product["tags"] else "Sin etiquetas"
            print(f"      {i+1}. {product['title']} - ${product['price']}")
            print(f"         Categoría: {product['category']['title']}")
            print(f"         Etiquetas: {tags_str}")
            print(f"         Imágenes: {len(product['pictures'])} imagen(es)")
        print()
        
        # Verificar categorías
        response = requests.get(f"{BASE_URL}/categories/", headers=HEADERS)
        categories = response.json()
        print(f"   📊 Total categorías: {len(categories)}")
        print("   📝 Categorías creadas:")
        for category in categories:
            picture_status = "✅ Con imagen" if category['picture'] else "❌ Sin imagen"
            print(f"      - {category['title']}: {category['description']} ({picture_status})")
        print()
        
        # Verificar etiquetas
        response = requests.get(f"{BASE_URL}/tags/", headers=HEADERS)
        tags = response.json()
        print(f"   📊 Total etiquetas: {len(tags)}")
        print("   📝 Etiquetas creadas:")
        for tag in tags:
            print(f"      - {tag['title']}")
        print()
        
        # Test 4: Verificar que las imágenes son accesibles
        print("4. Verificando accesibilidad de imágenes...")
        sample_product = products[0] if products else None
        if sample_product and sample_product['pictures']:
            image_url = f"{BASE_URL}{sample_product['pictures'][0]}"
            try:
                img_response = requests.head(image_url)
                if img_response.status_code == 200:
                    print(f"   ✅ Imagen accesible: {image_url}")
                else:
                    print(f"   ❌ Imagen no accesible: {image_url}")
            except:
                print(f"   ❌ Error accediendo a imagen: {image_url}")
        else:
            print("   ⚠️ No hay productos con imágenes para verificar")
        print()
        
        # Test 5: Probar seed una segunda vez (debe limpiar y recargar)
        print("5. Probando seed por segunda vez (debe limpiar datos anteriores)...")
        response = requests.post(f"{BASE_URL}/seed", headers=HEADERS)
        if response.status_code == 200:
            print("   ✅ Segundo seed ejecutado correctamente")
            
            # Verificar que los IDs cambiaron (datos fueron limpiados)
            response = requests.get(f"{BASE_URL}/products/", headers=HEADERS)
            new_products = response.json()
            print(f"   📊 Productos después del segundo seed: {len(new_products)}")
        else:
            print(f"   ❌ Error en segundo seed: {response.text}")
        print()
        
        print("🎉 ¡Todas las pruebas de seed completadas exitosamente!")
        print("📚 Los estudiantes pueden usar este endpoint para cargar datos de prueba rápidamente")
        print("🔗 Documentación completa en: http://localhost:8000/docs")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
        print("   Ejecuta: ./start.sh o uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_seed_functionality()
