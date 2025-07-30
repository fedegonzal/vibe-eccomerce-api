import yaml
import requests
import os
import uuid
from pathlib import Path
from urllib.parse import urlparse
from sqlalchemy.orm import Session
from typing import Dict, List, Any

import database
import crud
import schemas

def download_image(url: str, filename: str, uploads_dir: Path) -> str:
    """
    Descarga una imagen desde una URL y la guarda localmente.
    
    Args:
        url: URL de la imagen a descargar
        filename: Nombre base para el archivo
        uploads_dir: Directorio donde guardar la imagen
    
    Returns:
        Ruta local de la imagen descargada
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Obtener extensión del archivo desde la URL o usar jpg por defecto
        parsed_url = urlparse(url)
        path = parsed_url.path
        if '.' in path:
            extension = path.split('.')[-1].lower()
            # Validar extensiones de imagen
            if extension not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                extension = 'jpg'
        else:
            extension = 'jpg'
        
        # Generar nombre único para el archivo
        unique_filename = f"{filename}_{uuid.uuid4().hex[:8]}.{extension}"
        file_path = uploads_dir / unique_filename
        
        # Guardar la imagen
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        return f"/uploads/{unique_filename}"
    
    except Exception as e:
        print(f"Error descargando imagen {url}: {e}")
        return None

def clean_token_data(db: Session, token: str):
    """
    Limpia todos los datos (productos, categorías, etiquetas) para un token específico.
    
    Args:
        db: Sesión de base de datos
        token: Token del usuario
    """
    # Eliminar productos (esto también elimina las relaciones con etiquetas)
    products = db.query(database.Product).filter(database.Product.token == token).all()
    for product in products:
        db.delete(product)
    
    # Eliminar categorías
    categories = db.query(database.Category).filter(database.Category.token == token).all()
    for category in categories:
        db.delete(category)
    
    # Eliminar etiquetas
    tags = db.query(database.Tag).filter(database.Tag.token == token).all()
    for tag in tags:
        db.delete(tag)
    
    db.commit()

def load_seed_data(db: Session, token: str, seed_file_path: str = "seed.yml") -> Dict[str, Any]:
    """
    Carga datos desde el archivo seed.yml y los inserta en la base de datos.
    
    Args:
        db: Sesión de base de datos
        token: Token del usuario
        seed_file_path: Ruta al archivo de semilla
    
    Returns:
        Diccionario con estadísticas de la carga
    """
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    
    # Leer archivo YAML
    try:
        with open(seed_file_path, 'r', encoding='utf-8') as file:
            seed_data = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo de semilla no encontrado: {seed_file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error al parsear el archivo YAML: {e}")
    
    stats = {
        "categories_created": 0,
        "products_created": 0,
        "tags_created": 0,
        "images_downloaded": 0,
        "errors": []
    }
    
    # Crear un diccionario para almacenar las etiquetas creadas
    tags_map = {}
    
    # Procesar cada categoría
    for category_key, category_data in seed_data.items():
        try:
            # Crear categoría
            category_create = schemas.CategoryCreate(
                title=category_data["title"],
                description=category_data["description"]
            )
            
            db_category = crud.create_category(db=db, category=category_create, token=token)
            stats["categories_created"] += 1
            
            # Descargar imagen de categoría si existe
            if "picture" in category_data and category_data["picture"]:
                picture_url = download_image(
                    category_data["picture"],
                    f"category_{db_category.id}",
                    uploads_dir
                )
                if picture_url:
                    db_category.picture = picture_url
                    db.commit()
                    stats["images_downloaded"] += 1
            
            # Procesar productos de la categoría
            if "items" in category_data:
                for item_data in category_data["items"]:
                    try:
                        # Procesar etiquetas del producto
                        tag_ids = []
                        if "tags" in item_data:
                            for tag_name in item_data["tags"]:
                                if tag_name not in tags_map:
                                    # Crear nueva etiqueta
                                    tag_create = schemas.TagCreate(title=tag_name)
                                    db_tag = crud.create_tag(db=db, tag=tag_create, token=token)
                                    tags_map[tag_name] = db_tag.id
                                    stats["tags_created"] += 1
                                tag_ids.append(tags_map[tag_name])
                        
                        # Crear producto
                        product_create = schemas.ProductCreate(
                            title=item_data["title"],
                            description=item_data["description"],
                            price=float(item_data["price"]),
                            category_id=db_category.id,
                            tag_ids=tag_ids
                        )
                        
                        db_product = crud.create_product(db=db, product=product_create, token=token)
                        stats["products_created"] += 1
                        
                        # Descargar imágenes del producto
                        if "pictures" in item_data and item_data["pictures"]:
                            picture_urls = []
                            for i, picture_url in enumerate(item_data["pictures"]):
                                downloaded_url = download_image(
                                    picture_url,
                                    f"product_{db_product.id}_{i}",
                                    uploads_dir
                                )
                                if downloaded_url:
                                    picture_urls.append(downloaded_url)
                                    stats["images_downloaded"] += 1
                            
                            if picture_urls:
                                db_product.pictures = ",".join(picture_urls)
                                db.commit()
                    
                    except Exception as e:
                        error_msg = f"Error procesando producto '{item_data.get('title', 'sin título')}': {e}"
                        stats["errors"].append(error_msg)
                        print(error_msg)
        
        except Exception as e:
            error_msg = f"Error procesando categoría '{category_key}': {e}"
            stats["errors"].append(error_msg)
            print(error_msg)
    
    return stats
