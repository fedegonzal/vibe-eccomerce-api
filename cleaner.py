import os
import shutil
from pathlib import Path
from sqlalchemy.orm import Session
from typing import Dict, Any

import database

def clean_all_data(db: Session) -> Dict[str, Any]:
    """
    Limpia completamente la base de datos eliminando todos los registros.
    
    Args:
        db: Sesión de base de datos
    
    Returns:
        Diccionario con estadísticas de limpieza
    """
    stats = {
        "products_deleted": 0,
        "categories_deleted": 0,
        "tags_deleted": 0,
        "files_deleted": 0,
        "errors": []
    }
    
    try:
        # Contar registros antes de eliminar
        products_count = db.query(database.Product).count()
        categories_count = db.query(database.Category).count()
        tags_count = db.query(database.Tag).count()
        
        # Eliminar todos los productos (esto también elimina las relaciones con etiquetas)
        db.query(database.Product).delete()
        stats["products_deleted"] = products_count
        
        # Eliminar todas las categorías
        db.query(database.Category).delete()
        stats["categories_deleted"] = categories_count
        
        # Eliminar todas las etiquetas
        db.query(database.Tag).delete()
        stats["tags_deleted"] = tags_count
        
        # Confirmar cambios en la base de datos
        db.commit()
        
    except Exception as e:
        db.rollback()
        error_msg = f"Error limpiando base de datos: {e}"
        stats["errors"].append(error_msg)
        print(error_msg)
    
    return stats

def clean_uploaded_files() -> Dict[str, Any]:
    """
    Elimina todos los archivos subidos en el directorio uploads.
    
    Returns:
        Diccionario con estadísticas de archivos eliminados
    """
    stats = {
        "files_deleted": 0,
        "errors": []
    }
    
    uploads_dir = Path("uploads")
    
    try:
        if uploads_dir.exists() and uploads_dir.is_dir():
            # Contar archivos antes de eliminar
            files_list = list(uploads_dir.glob("*"))
            files_count = len([f for f in files_list if f.is_file()])
            
            # Eliminar todo el contenido del directorio
            shutil.rmtree(uploads_dir)
            
            # Recrear el directorio vacío
            uploads_dir.mkdir(exist_ok=True)
            
            stats["files_deleted"] = files_count
            print(f"Eliminados {files_count} archivos del directorio uploads/")
        else:
            print("Directorio uploads no existe o está vacío")
            
    except Exception as e:
        error_msg = f"Error limpiando archivos: {e}"
        stats["errors"].append(error_msg)
        print(error_msg)
    
    return stats

def clean_everything(db: Session) -> Dict[str, Any]:
    """
    Limpia completamente el sistema: base de datos y archivos subidos.
    
    Args:
        db: Sesión de base de datos
    
    Returns:
        Diccionario con estadísticas completas de limpieza
    """
    print("🧹 Iniciando limpieza completa del sistema...")
    
    # Limpiar base de datos
    db_stats = clean_all_data(db)
    
    # Limpiar archivos
    files_stats = clean_uploaded_files()
    
    # Combinar estadísticas
    combined_stats = {
        "products_deleted": db_stats["products_deleted"],
        "categories_deleted": db_stats["categories_deleted"],
        "tags_deleted": db_stats["tags_deleted"],
        "files_deleted": files_stats["files_deleted"],
        "errors": db_stats["errors"] + files_stats["errors"]
    }
    
    print("✅ Limpieza completa finalizada")
    return combined_stats
