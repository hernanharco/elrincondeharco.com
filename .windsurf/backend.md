# Backend - Auth Core con FastAPI y Neon PostgreSQL

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
    │   └── config.py             # Pydantic Settings v2 con computed_field
    ├── db/
    │   └── session.py            # AsyncEngine con psycopg 3
    ├── models/
    │   ├── __init__.py
    │   ├── base.py               # Base declarativa con imports automáticos
    │   └── example.py            # Modelo Example simple
    ├── schemas/
    │   ├── __init__.py
    │   ├── user.py               # Schemas para usuarios
    │   └── token.py              # Schemas para tokens
    ├── api/
    │   ├── __init__.py
    │   ├── route.py              # Router principal
    │   └── v1/
    │       ├── __init__.py
    │       └── endpoints/
    │           ├── __init__.py
    │           └── example.py     # Endpoints funcionales
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

### Base de Datos (`app/db/session.py`)
- **AsyncEngine** con psycopg 3
- `pool_pre_ping=True` para conexiones estables
- `AsyncSession` con `expire_on_commit=False`

### Modelos (`app/models/`)
- **Base declarativa** con imports automáticos
- Modelo **Example** con timestamps
- Estructura extensible para más modelos

### API (`app/api/`)
- Router principal con **include_router**
- Endpoints **v1** organizados
- Ejemplo funcional con CRUD básico

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

### ⚠️ Pendientes
- Crear archivo `.env` con credenciales Neon reales
- Probar conexión con base de datos real
- Implementar autenticación JWT
- Agregar más modelos y endpoints
- Tests unitarios completos

## 🚀 Próximos Pasos

1. **Configurar `.env`** con credenciales Neon
2. **Ejecutar `pnpm dev`** para iniciar servidor
3. **Verificar conexión** y creación de tablas
4. **Probar endpoints** en `http://localhost:8000/docs`
5. **Extender funcionalidad** según necesidades

## 📊 Endpoints Disponibles

- `GET /` - Mensaje de bienvenida
- `GET /health` - Health check general
- `GET /api/v1/example/` - Listar examples
- `POST /api/v1/example/` - Crear example
- `GET /api/v1/example/health` - Health check de ejemplo
- `GET /docs` - Documentación Swagger UI
- `GET /redoc` - Documentación ReDoc
