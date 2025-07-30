# API REST de Ecommerce - UNTDF

## Descripción

Esta aplicación es un ejemplo de una API REST simple para gestionar un ecommerce, diseñada para que los estudiantes de la Tecnicatura Universitaria en Desarrollo de Aplicaciones de la [Universidad Nacional de Tierra del Fuego](https://www.untdf.edu.ar/) puedan practicar con el desarrollo de Frontend y el consumo de APIs REST. Esta API fue desarrollada por el profesor Federico Gonzalez Brizzio, utilizando técnicas de Vibe Coding, con la ayuda de Copilot y agent Claude Sonnet 4, ambas herramientas gratuitas de inteligencia artificial.

## Propósito

Esta API permite a los estudiantes:
- Practicar el desarrollo de interfaces Frontend
- Aprender a consumir APIs REST
- Trabajar con operaciones CRUD (Create, Read, Update, Delete)
- Manejar autenticación mediante tokens
- Gestionar archivos e imágenes
- Integrar bases de datos relacionales

## Características

La API incluye las siguientes entidades:
- **Productos**: título, descripción, precio, categoría, imágenes, etiquetas
- **Categorías**: título, descripción, imagen
- **Etiquetas**: título

### Funcionalidades principales:
- CRUD completo para productos, categorías y etiquetas
- Aislamiento de datos por token de estudiante
- Subida y gestión de imágenes
- Base de datos SQLite
- Documentación automática con Swagger UI

## Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd ecommerce-api
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del servidor

Para ejecutar el servidor de desarrollo:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en:
- **URL principal**: http://localhost:8000
- **Documentación interactiva**: http://localhost:8000/docs
- **Documentación alternativa**: http://localhost:8000/redoc

## Uso de la API

### Autenticación

Todos los endpoints requieren un token Bearer en el header `Authorization`. Este token identifica a cada estudiante y aísla sus datos.

```bash
Authorization: Bearer tu_token_aqui
```

### Ejemplos con HTTPie

#### 1. Crear una categoría
```bash
http POST localhost:8000/categories/ \
  "Authorization:Bearer estudiante123" \
  title="Electrónicos" \
  description="Productos electrónicos y tecnología"
```

#### 2. Listar categorías
```bash
http GET localhost:8000/categories/ \
  "Authorization:Bearer estudiante123"
```

#### 3. Crear una etiqueta
```bash
http POST localhost:8000/tags/ \
  "Authorization:Bearer estudiante123" \
  title="Nuevo"
```

#### 4. Crear un producto
```bash
http POST localhost:8000/products/ \
  "Authorization:Bearer estudiante123" \
  title="iPhone 15" \
  description="Smartphone Apple último modelo" \
  price:=999.99 \
  category_id:=1 \
  tag_ids:='[1]'
```

#### 5. Subir imagen a un producto
```bash
http --form POST localhost:8000/products/1/pictures \
  "Authorization:Bearer estudiante123" \
  files@imagen.jpg
```

#### 6. Obtener un producto específico
```bash
http GET localhost:8000/products/1 \
  "Authorization:Bearer estudiante123"
```

#### 7. Actualizar un producto
```bash
http PUT localhost:8000/products/1 \
  "Authorization:Bearer estudiante123" \
  title="iPhone 15 Pro" \
  price:=1199.99
```

#### 8. Eliminar un producto
```bash
http DELETE localhost:8000/products/1 \
  "Authorization:Bearer estudiante123"
```

#### 9. Cargar datos de prueba (Seed)
```bash
http POST localhost:8000/seed \
  "Authorization:Bearer estudiante123"
```

**⚠️ Importante:** Este comando eliminará todos tus datos existentes y cargará datos de ejemplo desde el archivo `seed.yml`.

### Ejemplos con curl

#### Crear una categoría
```bash
curl -X POST "http://localhost:8000/categories/" \
  -H "Authorization: Bearer estudiante123" \
  -H "Content-Type: application/json" \
  -d '{"title": "Electrónicos", "description": "Productos electrónicos y tecnología"}'
```

#### Listar productos
```bash
curl -X GET "http://localhost:8000/products/" \
  -H "Authorization: Bearer estudiante123"
```

#### Cargar datos de prueba
```bash
curl -X POST "http://localhost:8000/seed" \
  -H "Authorization: Bearer estudiante123"
```

## Estructura de datos

### Producto
```json
{
  "id": 1,
  "title": "iPhone 15",
  "description": "Smartphone Apple último modelo",
  "price": 999.99,
  "category_id": 1,
  "pictures": ["/uploads/product_1_abc123.jpg"],
  "category": {
    "id": 1,
    "title": "Electrónicos",
    "description": "Productos electrónicos y tecnología",
    "picture": "/uploads/category_1_def456.jpg"
  },
  "tags": [
    {
      "id": 1,
      "title": "Nuevo"
    }
  ]
}
```

### Categoría
```json
{
  "id": 1,
  "title": "Electrónicos",
  "description": "Productos electrónicos y tecnología",
  "picture": "/uploads/category_1_def456.jpg"
}
```

### Etiqueta
```json
{
  "id": 1,
  "title": "Nuevo"
}
```

## Endpoints disponibles

### Categorías
- `GET /categories/` - Listar categorías
- `POST /categories/` - Crear categoría
- `GET /categories/{id}` - Obtener categoría específica
- `PUT /categories/{id}` - Actualizar categoría
- `DELETE /categories/{id}` - Eliminar categoría
- `POST /categories/{id}/picture` - Subir imagen a categoría

### Etiquetas
- `GET /tags/` - Listar etiquetas
- `POST /tags/` - Crear etiqueta
- `GET /tags/{id}` - Obtener etiqueta específica
- `PUT /tags/{id}` - Actualizar etiqueta
- `DELETE /tags/{id}` - Eliminar etiqueta

### Productos
- `GET /products/` - Listar productos
- `POST /products/` - Crear producto
- `GET /products/{id}` - Obtener producto específico
- `PUT /products/{id}` - Actualizar producto
- `DELETE /products/{id}` - Eliminar producto
- `POST /products/{id}/pictures` - Subir imágenes a producto

### Datos de Prueba
- `POST /seed` - Cargar datos de ejemplo y limpiar datos existentes

## Funcionalidad de Seed (Datos de Prueba)

### ¿Qué es el Seed?
El endpoint `/seed` permite a los estudiantes cargar rápidamente un conjunto completo de datos de prueba sin tener que crear manualmente cada categoría, producto y etiqueta. Es especialmente útil para:

- **Comenzar rápidamente**: Obtener datos listos para usar en segundos
- **Probar aplicaciones**: Tener contenido real para probar interfaces frontend
- **Demostraciones**: Mostrar funcionalidad con datos atractivos
- **Desarrollo**: No perder tiempo creando datos de prueba manualmente

### ¿Qué datos incluye?
El archivo `seed.yml` contiene:

**Categorías disponibles:**
- **Verduras**: Zanahoria, Zapallo, Tomate, Batata, Tomate Cherry, Remolacha, Berenjena, Repollo
- **Carnes**: Tapa de Asado, Pollo entero, Churrasco de Cerdo, Cordero, Roastbeef
- **Higiene**: Antitranspirante, Jabón líquido, Desodorante, Hojas de afeitar
- **Limpieza**: Limpiador multiuso, Papel higiénico, Lavandina, Detergente, Esponja

**Etiquetas incluidas:**
- "Promoción" - Para productos en oferta
- "Orgánico" - Para productos naturales
- "Producto local" - Para productos regionales

**Características especiales:**
- Todos los productos tienen precios realistas
- Cada producto incluye descripción detallada
- Las imágenes se descargan automáticamente desde internet
- Se crean relaciones automáticas entre productos, categorías y etiquetas

### ¿Cómo usar el Seed?

**⚠️ Advertencia importante:** El comando de seed **eliminará todos tus datos existentes** (productos, categorías, etiquetas) antes de cargar los nuevos.

```bash
# Con HTTPie
http POST localhost:8000/seed "Authorization:Bearer tu_token_unico"

# Con curl
curl -X POST "http://localhost:8000/seed" \
  -H "Authorization: Bearer tu_token_unico"
```

**Respuesta esperada:**
```json
{
  "message": "Datos de prueba cargados exitosamente",
  "statistics": {
    "categories_created": 4,
    "products_created": 20,
    "tags_created": 3,
    "images_downloaded": 25,
    "errors": []
  },
  "token": "tu_token_unico"
}
```

### Personalizar datos de Seed
Podés modificar el archivo `seed.yml` para agregar tus propios productos y categorías. El formato es simple y está documentado en el mismo archivo.

## Archivos e imágenes

Las imágenes se almacenan en la carpeta `uploads/` y son accesibles públicamente a través de la URL `/uploads/nombre_archivo`.

## Base de datos

La aplicación utiliza SQLite con el archivo `ecommerce.db` que se crea automáticamente al ejecutar la aplicación por primera vez.

## Desarrollo

Para desarrollo, se recomienda usar el flag `--reload` para que el servidor se reinicie automáticamente al detectar cambios:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Despliegue en Render.com

Esta aplicación está configurada para desplegarse en Render.com de forma gratuita. La configuración incluye:
- Puerto configurable mediante variable de entorno
- Archivos estáticos servidos correctamente
- Base de datos SQLite compatible

## Consideraciones importantes

1. **Tokens únicos**: Cada estudiante debe usar un token único para aislar sus datos
2. **Persistencia**: Los datos se mantienen entre reinicios del servidor
3. **Imágenes**: Las imágenes subidas son públicamente accesibles
4. **Límites**: Sin límites de rate limiting implementados (ideal para aprendizaje)

## Soporte

Para dudas o problemas, contactar al profesor Federico Gonzalez Brizzio por email: fgonzalez@untdf.edu.ar

---

**Universidad Nacional de Tierra del Fuego**  
Tecnicatura Universitaria en Desarrollo de Aplicaciones  
https://www.untdf.edu.ar/

## Archivos del proyecto

### Archivos principales
- `main.py` - Aplicación FastAPI principal con todos los endpoints
- `database.py` - Configuración de SQLite y modelos de datos
- `schemas.py` - Esquemas Pydantic para validación de datos
- `crud.py` - Operaciones de base de datos (Create, Read, Update, Delete)
- `auth.py` - Manejo de autenticación con tokens Bearer
- `seeder.py` - Funcionalidad para cargar datos de prueba

### Archivos de configuración
- `requirements.txt` - Dependencias de Python
- `seed.yml` - Datos de prueba para cargar con el endpoint `/seed`
- `start.sh` - Script para iniciar el servidor fácilmente
- `.gitignore` - Archivos a ignorar en control de versiones

### Archivos para deploy
- `Procfile` - Configuración para Render.com
- `runtime.txt` - Versión de Python para el deploy
- `render.yaml` - Configuración detallada de Render.com

### Scripts de prueba
- `test_api.py` - Script para probar todos los endpoints
- `test_seed.py` - Script específico para probar la funcionalidad de seed

### Directorios
- `uploads/` - Carpeta donde se almacenan las imágenes subidas
- `.venv/` - Entorno virtual de Python (se crea automáticamente)
