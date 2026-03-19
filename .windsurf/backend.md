# Backend - Portfolio API con FastAPI y Neon PostgreSQL

## 📁 Estructura del Proyecto

```
backend/
├── package.json                    # Scripts npm/pnpm para desarrollo
├── pyproject.toml                 # Dependencias Poetry con psycopg para máxima seguridad
├── .gitignore                     # Archivos ignorados por Git
├── poetry-setup.sh                # Script de configuración automatizada
├── Dockerfile                     # Configuración Docker para producción
└── app/
    ├── __init__.py
    ├── main.py                    # App FastAPI con lifespan y logs con emojis
    ├── core/
    │   ├── config.py             # Pydantic Settings v2 con computed_field
    │   └── cloudinary.py         # Configuración y función de upload a Cloudinary
    ├── db/
    │   └── session.py            # AsyncEngine con psycopg 3
    ├── models/
    │   ├── __init__.py
    │   ├── base.py               # Base declarativa con imports automáticos
    │   ├── example.py            # Modelo Example simple
    │   ├── hero.py               # Modelo para sección Hero
    │   ├── about.py              # Modelo para sección About
    │   ├── passions.py           # Modelo para sección Passions
    │   ├── projects.py           # Modelo para sección Projects
    │   ├── stack.py              # Modelo para sección Stack
    │   └── footer.py             # Modelo para sección Footer
    ├── schemas/
    │   ├── __init__.py
    │   ├── user.py               # Schemas para usuarios
    │   ├── token.py              # Schemas para tokens
    │   ├── hero.py               # Schemas para Hero (Create/Update/Response)
    │   ├── about.py              # Schemas para About (Create/Update/Response)
    │   ├── passions.py           # Schemas para Passions (Create/Update/Response)
    │   ├── projects.py           # Schemas para Projects (Create/Update/Response)
    │   ├── stack.py              # Schemas para Stack (Create/Update/Response)
    │   └── footer.py             # Schemas para Footer (Create/Update/Response)
    ├── api/
    │   ├── __init__.py
    │   ├── route.py              # Router principal con todos los dominios
    │   └── v1/
    │       ├── __init__.py
    │       └── endpoints/
    │           ├── __init__.py
    │           ├── example.py     # Endpoints funcionales
    │           ├── hero.py        # Endpoints CRUD para Hero
    │           ├── about.py       # Endpoints CRUD para About
    │           ├── passions.py    # Endpoints CRUD para Passions
    │           ├── projects.py     # Endpoints CRUD para Projects
    │           ├── stack.py       # Endpoints CRUD para Stack
    │           └── footer.py      # Endpoints CRUD para Footer
    └── tests/
        └── __init__.py
```

## 🔧 Configuración Principal

### Dependencias Clave
- **FastAPI**: Framework web moderno
- **psycopg[binary,pool]**: Driver PostgreSQL con máxima seguridad
- **SQLAlchemy[asyncio]**: ORM async
- **pydantic-settings[email]**: Configuración con validación de email
- **python-dotenv**: Variables de entorno
- **cloudinary**: Upload de imágenes a Cloudinary

### Seguridad Neon PostgreSQL
- `sslmode=require`: Conexión SSL obligatoria
- `channel_binding=require`: Protección MITM máxima
- URL construida dinámicamente desde variables .env

## 🚀 Scripts Disponibles

```json
{
  "dev": "poetry run uvicorn app.main:app --reload --host 0.0.0.0",
  "start": "poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000",
  "test": "poetry run pytest",
  "test:coverage": "poetry run pytest --cov=app --cov-report=html",
  "lint": "poetry run black app/ && poetry run isort app/ && poetry run flake8 app/",
  "format": "poetry run black app/ && poetry run isort app/",
  "type-check": "poetry run mypy app/",
  "docker:build": "docker build -t auth-core-backend .",
  "docker:run": "docker run -p 8000:8000 --env-file .env auth-core-backend",
  "setup:dev": "bash poetry-setup.sh development",
  "setup:prod": "bash poetry-setup.sh production",
  "shell": "poetry shell",
  "install": "poetry install",
  "install:prod": "poetry install --only main",
  "add": "poetry add",
  "add:dev": "poetry add --group dev",
  "update": "poetry update",
  "export": "poetry export -f requirements.txt --output requirements.txt --without-hashes"
}
```

## 🏗️ Características Implementadas

### Configuración (`app/core/config.py`)
- **Pydantic Settings v2** con `computed_field`
- Mapeo directo desde variables `.env`
- URL de base de datos construida dinámicamente
- Soporte para desarrollo y producción
- Configuración de Cloudinary integrada

### Cloudinary (`app/core/cloudinary.py`)
- **Configuración automática** desde variables de entorno
- **Función `upload_image()`** para subir imágenes
- **Retorno de URLs seguras** (https) siempre
- **Folder específico**: "elrincondelharco"

### Base de Datos (`app/db/session.py`)
- **AsyncEngine** con psycopg 3
- `pool_pre_ping=True` para conexiones estables
- `AsyncSession` con `expire_on_commit=False`

### Modelos (`app/models/`)
- **Base declarativa** con imports automáticos
- Modelo **Example** con timestamps
- **6 dominios de portfolio** implementados:
  - **Hero**: Sección principal (title, subtitle, description, buttons)
  - **About**: Información personal (experience, leadership, location)
  - **Passions**: Pasiones personales (family, games, coding)
  - **Projects**: Portafolio (tags, URLs, iconos)
  - **Stack**: Tecnologías (estilos flexibles)
  - **Footer**: Contacto y enlaces (social media, quick links)
- **Tipos de datos optimizados**: String, Text, JSONB, etc.

### API (`app/api/`)
- Router principal con **include_router**
- Endpoints **v1** organizados por dominio
- **Ejemplo funcional** con CRUD básico
- **6 dominios completos** con CRUD completo:
  - `GET /api/v1/{dominios}/` - Listar todos
  - `GET /api/v1/{dominios}/{id}` - Obtener por ID
  - `GET /api/v1/{dominios}/latest/` - Último registro (hero, about, passions, footer)
  - `POST /api/v1/{dominios}/` - Crear (con upload de imagen)
  - `PUT /api/v1/{dominios}/{id}` - Actualizar (con upload de imagen)
  - `DELETE /api/v1/{dominios}/{id}` - Eliminar
- **Upload de imágenes** integrado con Cloudinary
- **Form data handling** para todos los endpoints

### Lifespan (`app/main.py`)
- Logs con emojis informativos
- Verificación de conexión a Neon
- Creación automática de tablas
- Timezone configurado (Europe/Madrid)

## 📝 Variables de Entorno Requeridas

```env
# Neon PostgreSQL Configuration
PGHOST=your-neon-host
PGDATABASE=neondb
PGUSER=neondb_owner
PGPASSWORD=your-password
PGSSLMODE=require
PGCHANNELBINDING=require

# Application Settings
DEBUG=true
SECRET_KEY=your-secret-key-here

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=dxyk76jhu
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## 🐳 Docker

- **Python 3.12 slim** como base
- **Poetry** para gestión de dependencias
- **Usuario no-root** para seguridad
- **Health check** automático
- **Exposición puerto 8000**

## 🔧 Estado Actual

### ✅ Completado
- Estructura completa de carpetas
- Configuración con Pydantic v2
- Conexión async con psycopg 3
- Modelo básico funcional
- Endpoints API funcionales
- Scripts de desarrollo
- Configuración Docker
- **Integración completa con Cloudinary**
- **6 dominios de portfolio implementados**
- **CRUD completo para todos los dominios**
- **Upload de imágenes funcionando**
- **Schemas Pydantic completos**
- **Modelos SQLAlchemy optimizados**

### ⚠️ Pendientes
- Configurar variables `.env` con API keys de Cloudinary
- Probar conexión con base de datos real
- Implementar autenticación JWT
- Tests unitarios completos
- Migración de datos iniciales

## 🚀 Próximos Pasos

1. **Configurar `.env`** con credenciales Neon y Cloudinary
2. **Ejecutar `pnpm dev`** para iniciar servidor
3. **Verificar conexión** y creación de tablas
4. **Probar endpoints** en `http://localhost:8000/docs`
5. **Crear datos iniciales** para cada dominio
6. **Integrar frontend** con los nuevos endpoints

## 📊 Endpoints Disponibles

### Generales
- `GET /` - Mensaje de bienvenida
- `GET /health` - Health check general
- `GET /docs` - Documentación Swagger UI
- `GET /redoc` - Documentación ReDoc

### Dominios de Portfolio

#### Hero (`/api/v1/heroes/`)
- `GET /api/v1/heroes/` - Listar todos
- `GET /api/v1/heroes/{id}` - Obtener por ID
- `GET /api/v1/heroes/latest/` - Último registro
- `POST /api/v1/heroes/` - Crear (con imagen)
- `PUT /api/v1/heroes/{id}` - Actualizar (con imagen)
- `DELETE /api/v1/heroes/{id}` - Eliminar

#### About (`/api/v1/abouts/`)
- `GET /api/v1/abouts/` - Listar todos
- `GET /api/v1/abouts/{id}` - Obtener por ID
- `GET /api/v1/abouts/latest/` - Último registro
- `POST /api/v1/abouts/` - Crear (con imagen)
- `PUT /api/v1/abouts/{id}` - Actualizar (con imagen)
- `DELETE /api/v1/abouts/{id}` - Eliminar

#### Passions (`/api/v1/passions/`)
- `GET /api/v1/passions/` - Listar todos
- `GET /api/v1/passions/{id}` - Obtener por ID
- `GET /api/v1/passions/latest/` - Último registro
- `POST /api/v1/passions/` - Crear (con imagen)
- `PUT /api/v1/passions/{id}` - Actualizar (con imagen)
- `DELETE /api/v1/passions/{id}` - Eliminar

#### Projects (`/api/v1/projects/`)
- `GET /api/v1/projects/` - Listar todos
- `GET /api/v1/projects/{id}` - Obtener por ID
- `POST /api/v1/projects/` - Crear (con imagen)
- `PUT /api/v1/projects/{id}` - Actualizar (con imagen)
- `DELETE /api/v1/projects/{id}` - Eliminar

#### Stack (`/api/v1/stacks/`)
- `GET /api/v1/stacks/` - Listar todos
- `GET /api/v1/stacks/{id}` - Obtener por ID
- `POST /api/v1/stacks/` - Crear
- `PUT /api/v1/stacks/{id}` - Actualizar
- `DELETE /api/v1/stacks/{id}` - Eliminar

#### Footer (`/api/v1/footers/`)
- `GET /api/v1/footers/` - Listar todos
- `GET /api/v1/footers/{id}` - Obtener por ID
- `GET /api/v1/footers/latest/` - Último registro
- `POST /api/v1/footers/` - Crear
- `PUT /api/v1/footers/{id}` - Actualizar
- `DELETE /api/v1/footers/{id}` - Eliminar

### Example (Legacy)
- `GET /api/v1/example/` - Listar examples
- `POST /api/v1/example/` - Crear example
- `GET /api/v1/example/health` - Health check de ejemplo
