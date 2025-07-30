from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

import database
import schemas
import crud
import seeder
import cleaner
from auth import get_current_token

# Create FastAPI app
app = FastAPI(
    title="API REST de Ecommerce - UNTDF",
    description="""
    ## API REST simple para gestionar un ecommerce
    
    Esta API fue desarrollada para que los estudiantes de la **Tecnicatura Universitaria en Desarrollo de Aplicaciones** 
    de la Universidad Nacional de Tierra del Fuego puedan practicar con el desarrollo de Frontend y el consumo de APIs REST.
    
    ### Características principales:
    * **Productos**: Gestión completa de productos con título, descripción, precio, categoría, imágenes y etiquetas
    * **Categorías**: Organización de productos por categorías con imagen descriptiva
    * **Etiquetas**: Sistema de etiquetado para clasificación adicional
    * **Autenticación**: Sistema de tokens para aislar datos entre estudiantes
    * **Subida de archivos**: Gestión de imágenes para productos y categorías
    
    ### Autenticación
    Todos los endpoints requieren un token Bearer en el header `Authorization`:
    ```
    Authorization: Bearer tu_token_unico
    ```
    
    ### Universidad Nacional de Tierra del Fuego
    Desarrollado por el Prof. Federico Gonzalez Brizzio  
    📧 fgonzalez@untdf.edu.ar  
    🌐 https://www.untdf.edu.ar/
    """,
    version="1.0.0",
    contact={
        "name": "Prof. Federico Gonzalez Brizzio",
        "email": "fgonzalez@untdf.edu.ar",
        "url": "https://www.untdf.edu.ar/",
    },
    license_info={
        "name": "Uso Educativo - UNTDF",
        "url": "https://www.untdf.edu.ar/",
    },
)

# Create database tables
database.create_tables()

# Create uploads directory
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)

# Mount static files for serving images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Admin token verification
def verify_admin_token(token: str) -> bool:
    """Verifica si el token corresponde al administrador"""
    admin_token = os.getenv("ADMIN_TOKEN")
    return admin_token and token == admin_token

def get_admin_token(credentials = Depends(get_current_token)) -> str:
    """Dependency para verificar token de administrador"""
    if not verify_admin_token(credentials):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token de administrador requerido"
        )
    return credentials

# Root endpoint
@app.get(
    "/",
    summary="Información de la API",
    description="Endpoint principal que proporciona información básica sobre la API de Ecommerce de la UNTDF",
    tags=["Información General"]
)
def read_root():
    """
    ## Bienvenido a la API de Ecommerce - UNTDF
    
    Esta API permite gestionar un sistema de ecommerce simple para práctica educativa.
    
    **Enlaces útiles:**
    - Documentación interactiva: `/docs`
    - Documentación alternativa: `/redoc`
    - Universidad: https://www.untdf.edu.ar/
    """
    return {
        "message": "API REST de Ecommerce - Universidad Nacional de Tierra del Fuego",
        "version": "1.0.0",
        "docs": "/docs",
        "universidad": "https://www.untdf.edu.ar/",
        "contacto": "fgonzalez@untdf.edu.ar"
    }

# Category endpoints
@app.get(
    "/categories/", 
    response_model=List[schemas.Category],
    summary="Listar categorías",
    description="Obtiene todas las categorías del estudiante autenticado con paginación opcional",
    tags=["Categorías"]
)
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Listar todas las categorías
    
    Obtiene una lista de todas las categorías creadas por el estudiante autenticado.
    
    **Parámetros:**
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a devolver
    
    **Respuesta:**
    Lista de categorías con sus respectivos datos e imagen (si tiene)
    """
    categories = crud.get_categories(db, token=token, skip=skip, limit=limit)
    return categories

@app.post(
    "/categories/", 
    response_model=schemas.Category,
    summary="Crear categoría",
    description="Crea una nueva categoría de productos",
    tags=["Categorías"]
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Crear una nueva categoría
    
    Crea una nueva categoría que podrá ser utilizada para organizar productos.
    
    **Datos requeridos:**
    - **title**: Nombre de la categoría (ej: "Electrónicos")
    - **description**: Descripción detallada de la categoría
    
    **Nota:** La imagen se puede agregar posteriormente usando el endpoint de subida de imagen.
    """
    return crud.create_category(db=db, category=category, token=token)

@app.get(
    "/categories/{category_id}", 
    response_model=schemas.Category,
    summary="Obtener categoría específica",
    description="Obtiene los detalles de una categoría específica por su ID",
    tags=["Categorías"]
)
def read_category(
    category_id: int,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Obtener una categoría específica
    
    Obtiene todos los detalles de una categoría específica usando su ID.
    
    **Parámetros:**
    - **category_id**: ID único de la categoría a obtener
    
    **Respuesta:**
    Datos completos de la categoría incluyendo imagen si tiene una asignada.
    """
    db_category = crud.get_category(db, category_id=category_id, token=token)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_category

@app.put(
    "/categories/{category_id}", 
    response_model=schemas.Category,
    summary="Actualizar categoría",
    description="Actualiza los datos de una categoría existente",
    tags=["Categorías"]
)
def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Actualizar una categoría
    
    Actualiza los datos de una categoría existente. Se pueden actualizar campos individuales.
    
    **Parámetros:**
    - **category_id**: ID de la categoría a actualizar
    - **title**: Nuevo nombre de la categoría (opcional)
    - **description**: Nueva descripción de la categoría (opcional)
    
    **Respuesta:**
    Datos actualizados de la categoría.
    """
    db_category = crud.update_category(db, category_id=category_id, category=category, token=token)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_category

@app.delete(
    "/categories/{category_id}",
    summary="Eliminar categoría",
    description="Elimina una categoría del sistema",
    tags=["Categorías"]
)
def delete_category(
    category_id: int,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Eliminar una categoría
    
    Elimina permanentemente una categoría del sistema.
    
    **⚠️ Advertencia:** Esta acción no se puede deshacer.
    
    **Parámetros:**
    - **category_id**: ID de la categoría a eliminar
    
    **Nota:** Asegúrate de que no haya productos asociados a esta categoría antes de eliminarla.
    """
    db_category = crud.delete_category(db, category_id=category_id, token=token)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada exitosamente"}

@app.post(
    "/categories/{category_id}/picture",
    summary="Subir imagen a categoría",
    description="Sube una imagen para representar visualmente la categoría",
    tags=["Categorías", "Archivos"]
)
def upload_category_picture(
    category_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Subir imagen a una categoría
    
    Permite subir una imagen que representará visualmente la categoría en el frontend.
    
    **Parámetros:**
    - **category_id**: ID de la categoría donde subir la imagen
    - **file**: Archivo de imagen (JPEG, PNG, etc.)
    
    **Formatos soportados:**
    - JPEG (.jpg, .jpeg)
    - PNG (.png)
    - GIF (.gif)
    
    **Respuesta:**
    URL pública donde se puede acceder a la imagen subida.
    """
    # Check if category exists
    db_category = crud.get_category(db, category_id=category_id, token=token)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    filename = f"category_{category_id}_{uuid.uuid4()}.{file_extension}"
    file_path = uploads_dir / filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update category with picture path
    db_category.picture = f"/uploads/{filename}"
    db.commit()
    db.refresh(db_category)
    
    return {"picture_url": f"/uploads/{filename}"}

# Tag endpoints
@app.get(
    "/tags/", 
    response_model=List[schemas.Tag],
    summary="Listar etiquetas",
    description="Obtiene todas las etiquetas del estudiante autenticado",
    tags=["Etiquetas"]
)
def read_tags(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Listar todas las etiquetas
    
    Obtiene una lista de todas las etiquetas creadas por el estudiante autenticado.
    Las etiquetas se usan para clasificar y filtrar productos.
    
    **Parámetros:**
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a devolver
    
    **Ejemplos de etiquetas:**
    - "Nuevo", "Oferta", "Destacado", "Liquidación", etc.
    """
    tags = crud.get_tags(db, token=token, skip=skip, limit=limit)
    return tags

@app.post(
    "/tags/", 
    response_model=schemas.Tag,
    summary="Crear etiqueta",
    description="Crea una nueva etiqueta para clasificar productos",
    tags=["Etiquetas"]
)
def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Crear una nueva etiqueta
    
    Crea una nueva etiqueta que puede ser asignada a productos para clasificación adicional.
    
    **Datos requeridos:**
    - **title**: Nombre de la etiqueta (ej: "Nuevo", "Oferta", "Destacado")
    
    **Casos de uso:**
    - Marcar productos en oferta
    - Destacar productos nuevos
    - Crear filtros especiales
    """
    return crud.create_tag(db=db, tag=tag, token=token)

@app.get(
    "/tags/{tag_id}", 
    response_model=schemas.Tag,
    summary="Obtener etiqueta específica",
    description="Obtiene los detalles de una etiqueta específica por su ID",
    tags=["Etiquetas"]
)
def read_tag(
    tag_id: int,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Obtener una etiqueta específica
    
    Obtiene los detalles de una etiqueta específica usando su ID.
    
    **Parámetros:**
    - **tag_id**: ID único de la etiqueta a obtener
    """
    db_tag = crud.get_tag(db, tag_id=tag_id, token=token)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    return db_tag

@app.put(
    "/tags/{tag_id}", 
    response_model=schemas.Tag,
    summary="Actualizar etiqueta",
    description="Actualiza el nombre de una etiqueta existente",
    tags=["Etiquetas"]
)
def update_tag(
    tag_id: int,
    tag: schemas.TagUpdate,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Actualizar una etiqueta
    
    Actualiza el nombre de una etiqueta existente.
    
    **Parámetros:**
    - **tag_id**: ID de la etiqueta a actualizar
    - **title**: Nuevo nombre de la etiqueta
    """
    db_tag = crud.update_tag(db, tag_id=tag_id, tag=tag, token=token)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    return db_tag

@app.delete(
    "/tags/{tag_id}",
    summary="Eliminar etiqueta",
    description="Elimina una etiqueta del sistema",
    tags=["Etiquetas"]
)
def delete_tag(
    tag_id: int,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Eliminar una etiqueta
    
    Elimina permanentemente una etiqueta del sistema.
    
    **⚠️ Advertencia:** Esta acción no se puede deshacer.
    
    **Parámetros:**
    - **tag_id**: ID de la etiqueta a eliminar
    
    **Nota:** La etiqueta se desasociará automáticamente de todos los productos que la tenían asignada.
    """
    db_tag = crud.delete_tag(db, tag_id=tag_id, token=token)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    return {"message": "Etiqueta eliminada exitosamente"}

# Product endpoints
@app.get(
    "/products/", 
    response_model=List[schemas.Product],
    summary="Listar productos",
    description="Obtiene todos los productos del estudiante autenticado con sus categorías y etiquetas",
    tags=["Productos"]
)
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Listar todos los productos
    
    Obtiene una lista completa de productos con toda su información relacionada:
    categoría, etiquetas e imágenes.
    
    **Parámetros:**
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a devolver
    
    **Respuesta incluye:**
    - Información básica del producto (título, descripción, precio)
    - Categoría completa con su información
    - Lista de etiquetas asignadas
    - URLs de las imágenes del producto
    """
    products = crud.get_products(db, token=token, skip=skip, limit=limit)
    # Convert pictures string to list
    for product in products:
        if product.pictures:
            product.pictures = product.pictures.split(",")
        else:
            product.pictures = []
    return products

@app.post(
    "/products/", 
    response_model=schemas.Product,
    summary="Crear producto",
    description="Crea un nuevo producto en el catálogo",
    tags=["Productos"]
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Crear un nuevo producto
    
    Crea un nuevo producto en el catálogo con toda su información.
    
    **Datos requeridos:**
    - **title**: Nombre del producto
    - **description**: Descripción detallada
    - **price**: Precio en números decimales
    - **category_id**: ID de la categoría a la que pertenece
    - **tag_ids**: Lista de IDs de etiquetas (opcional)
    
    **Ejemplo:**
    ```json
    {
        "title": "iPhone 15 Pro",
        "description": "Smartphone Apple con chip A17 Pro",
        "price": 1199.99,
        "category_id": 1,
        "tag_ids": [1, 2]
    }
    ```
    
    **Nota:** Las imágenes se pueden agregar posteriormente usando el endpoint de subida de imágenes.
    """
    # Check if category exists
    category = crud.get_category(db, product.category_id, token)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db_product = crud.create_product(db=db, product=product, token=token)
    # Convert pictures string to list for response
    if db_product.pictures:
        db_product.pictures = db_product.pictures.split(",")
    else:
        db_product.pictures = []
    return db_product

@app.get(
    "/products/{product_id}", 
    response_model=schemas.Product,
    summary="Obtener producto específico",
    description="Obtiene todos los detalles de un producto específico",
    tags=["Productos"]
)
def read_product(
    product_id: int,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Obtener un producto específico
    
    Obtiene todos los detalles de un producto incluyendo:
    - Información básica (título, descripción, precio)
    - Categoría completa
    - Lista de etiquetas
    - URLs de todas las imágenes
    
    **Parámetros:**
    - **product_id**: ID único del producto a obtener
    """
    db_product = crud.get_product(db, product_id=product_id, token=token)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Convert pictures string to list
    if db_product.pictures:
        db_product.pictures = db_product.pictures.split(",")
    else:
        db_product.pictures = []
    return db_product

@app.put(
    "/products/{product_id}", 
    response_model=schemas.Product,
    summary="Actualizar producto",
    description="Actualiza los datos de un producto existente",
    tags=["Productos"]
)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Actualizar un producto
    
    Actualiza cualquier campo de un producto existente. Solo se actualizarán los campos proporcionados.
    
    **Parámetros:**
    - **product_id**: ID del producto a actualizar
    - **title**: Nuevo título (opcional)
    - **description**: Nueva descripción (opcional)
    - **price**: Nuevo precio (opcional)
    - **category_id**: Nueva categoría (opcional)
    - **tag_ids**: Nueva lista de etiquetas (opcional)
    
    **Ejemplo de actualización parcial:**
    ```json
    {
        "price": 1099.99,
        "tag_ids": [1, 3, 5]
    }
    ```
    """
    # Check if category exists if provided
    if product.category_id:
        category = crud.get_category(db, product.category_id, token)
        if not category:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db_product = crud.update_product(db, product_id=product_id, product=product, token=token)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Convert pictures string to list
    if db_product.pictures:
        db_product.pictures = db_product.pictures.split(",")
    else:
        db_product.pictures = []
    return db_product

@app.delete(
    "/products/{product_id}",
    summary="Eliminar producto",
    description="Elimina un producto del catálogo",
    tags=["Productos"]
)
def delete_product(
    product_id: int,
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Eliminar un producto
    
    Elimina permanentemente un producto del catálogo incluyendo todas sus imágenes asociadas.
    
    **⚠️ Advertencia:** Esta acción no se puede deshacer.
    
    **Parámetros:**
    - **product_id**: ID del producto a eliminar
    
    **Nota:** Las imágenes del producto también serán eliminadas del servidor.
    """
    db_product = crud.delete_product(db, product_id=product_id, token=token)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado exitosamente"}

@app.post(
    "/products/{product_id}/pictures",
    summary="Subir imágenes al producto",
    description="Sube una o múltiples imágenes para mostrar el producto",
    tags=["Productos", "Archivos"]
)
def upload_product_pictures(
    product_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Subir imágenes a un producto
    
    Permite subir una o múltiples imágenes para mostrar el producto desde diferentes ángulos.
    
    **Parámetros:**
    - **product_id**: ID del producto donde subir las imágenes
    - **files**: Lista de archivos de imagen
    
    **Formatos soportados:**
    - JPEG (.jpg, .jpeg)
    - PNG (.png)
    - GIF (.gif)
    
    **Buenas prácticas:**
    - Usar imágenes de alta calidad
    - Mostrar el producto desde diferentes ángulos
    - Incluir imágenes de detalles importantes
    
    **Respuesta:**
    Lista de URLs públicas donde se pueden acceder a las imágenes subidas.
    """
    # Check if product exists
    db_product = crud.get_product(db, product_id=product_id, token=token)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    picture_urls = []
    
    for file in files:
        # Generate unique filename
        file_extension = file.filename.split(".")[-1]
        filename = f"product_{product_id}_{uuid.uuid4()}.{file_extension}"
        file_path = uploads_dir / filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        picture_urls.append(f"/uploads/{filename}")
    
    # Update product with picture paths
    existing_pictures = db_product.pictures.split(",") if db_product.pictures else []
    all_pictures = existing_pictures + picture_urls
    db_product.pictures = ",".join(all_pictures)
    db.commit()
    db.refresh(db_product)
    
    return {"picture_urls": picture_urls}

# Seed endpoint
@app.post(
    "/seed",
    summary="Cargar datos de prueba",
    description="Limpia todos los datos del token y carga datos de prueba desde seed.yml",
    tags=["Datos de Prueba"]
)
def seed_database(
    db: Session = Depends(database.get_db),
    token: str = Depends(get_current_token)
):
    """
    ## Cargar datos de prueba desde seed.yml
    
    Este endpoint permite a los estudiantes cargar rápidamente un conjunto de datos de prueba 
    para practicar con la API sin tener que crear manualmente categorías, productos y etiquetas.
    
    **⚠️ Advertencia:** Este endpoint eliminará TODOS los datos existentes para tu token 
    (productos, categorías y etiquetas) antes de cargar los nuevos datos.
    
    **Qué hace:**
    1. Elimina todos los productos, categorías y etiquetas de tu token
    2. Lee el archivo `seed.yml` con datos de ejemplo
    3. Crea nuevas categorías, productos y etiquetas
    4. Descarga automáticamente todas las imágenes desde internet
    5. Las guarda localmente en el servidor
    
    **Datos incluidos en seed.yml:**
    - **Verduras**: Zanahoria, Zapallo, Tomate, Batata, etc.
    - **Carnes**: Tapa de asado, Pollo, Churrasco, Cordero, etc.
    - **Higiene**: Antitranspirante, Jabón, Desodorante, etc.
    - **Limpieza**: Limpiador, Papel higiénico, Lavandina, etc.
    
    **Etiquetas incluidas:**
    - "Promoción", "Orgánico", "Producto local"
    
    **Uso recomendado:**
    - Ideal para comenzar rápidamente con datos de ejemplo
    - Perfecto para probar tu aplicación frontend
    - Útil para demostraciones y pruebas
    
    **Respuesta:**
    Estadísticas detalladas sobre los datos cargados y errores si los hubiera.
    """
    try:
        # Limpiar datos existentes
        seeder.clean_token_data(db, token)
        
        # Cargar nuevos datos desde seed.yml
        stats = seeder.load_seed_data(db, token)
        
        return {
            "message": "Datos de prueba cargados exitosamente",
            "statistics": stats,
            "token": token
        }
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=404, 
            detail="Archivo seed.yml no encontrado. Asegúrate de que el archivo existe en el directorio raíz."
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor al cargar datos: {str(e)}"
        )

# Clean endpoint (internal use only)
@app.post(
    "/clean",
    summary="Limpiar sistema completo (Administrador)",
    description="Elimina todos los datos y archivos del sistema. Requiere token de administrador.",
    tags=["Administración"]
)
def clean_system(
    db: Session = Depends(database.get_db),
    admin_token: str = Depends(get_admin_token)
):
    """
    ## Limpiar sistema completo (Solo Administrador)
    
    Este endpoint elimina TODOS los datos y archivos del sistema de forma permanente.
    
    **🔒 Seguridad:**
    - Requiere token de administrador especial definido en variable de entorno `ADMIN_TOKEN`
    - Los estudiantes NO tienen acceso a este token
    - Solo para uso administrativo
    
    **⚠️ PELIGRO:** Este endpoint eliminará:
    - Todos los productos de todos los estudiantes
    - Todas las categorías de todos los estudiantes  
    - Todas las etiquetas de todos los estudiantes
    - Todos los archivos de imágenes subidos
    
    **Casos de uso:**
    - Limpiar el sistema al final del semestre
    - Resetear la base de datos para nuevos estudiantes
    - Mantenimiento general del sistema
    - Preparar ambiente para nuevas clases
    
    **Respuesta:**
    Estadísticas detalladas de todos los elementos eliminados.
    """
    """
    Endpoint interno para limpieza completa del sistema.
    Requiere token de administrador definido en variable de entorno ADMIN_TOKEN.
    
    ⚠️ PELIGRO: Este endpoint eliminará TODOS los datos y archivos del sistema.
    """
    try:
        stats = cleaner.clean_everything(db)
        
        return {
            "message": "Sistema limpiado completamente",
            "statistics": stats,
            "warning": "Todos los datos y archivos han sido eliminados"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor durante la limpieza: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
