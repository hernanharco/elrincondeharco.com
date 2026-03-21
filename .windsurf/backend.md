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
    ├── main.py                    # App FastAPI con lifespan, CORS y logs con emojis
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
    │   ├── footer.py             # Modelo para sección Footer
    │   └── site_settings.py      # Modelo para configuración del sitio
    ├── schemas/
    │   ├── __init__.py
    │   ├── user.py               # Schemas para usuarios
    │   ├── token.py              # Schemas para tokens
    │   ├── hero.py               # Schemas para Hero (Create/Update/Response)
    │   ├── about.py              # Schemas para About (Create/Update/Response)
    │   ├── passions.py           # Schemas para Passions (Create/Update/Response)
    │   ├── projects.py           # Schemas para Projects (Create/Update/Response)
    │   ├── stack.py              # Schemas para Stack (Create/Update/Response)
    │   ├── footer.py             # Schemas para Footer (Create/Update/Response)
    │   └── site_settings.py      # Schemas para SiteSettings (Create/Update/Response)
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
    │           ├── footer.py      # Endpoints CRUD para Footer
    │           └── site_settings.py # Endpoints CRUD para SiteSettings
    └── tests/
        └── __init__.py
```

## 🔧 Configuración Principal

### Dependencias Clave
- **FastAPI**: Framework web moderno con CORS integrado
- **psycopg[binary,pool]**: Driver PostgreSQL con máxima seguridad
- **SQLAlchemy[asyncio]**: ORM async con pool de conexiones
- **pydantic-settings[email]**: Configuración con validación de email
- **python-dotenv**: Variables de entorno
- **cloudinary**: Upload de imágenes a Cloudinary

### Seguridad Neon PostgreSQL
- `sslmode=require`: Conexión SSL obligatoria
- `channel_binding=require`: Protección MITM máxima
- URL construida dinámicamente desde variables .env
- Pool de conexiones con `pool_pre_ping=True`

### CORS Configurado
- **Orígenes permitidos**: `http://localhost:4321` (frontend Astro)
- **Métodos**: GET, POST, PUT, DELETE, OPTIONS
- **Headers**: Content-Type, Authorization
- **Credentials**: Soportado para futura autenticación

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
  "export": "poetry export -f requirements.txt --output requirements.txt --without-hashes",
  "seed": "poetry run python -m app.db.seed"
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
- **Función `upload_image()`** para subir imágenes y PDFs
- **Retorno de URLs seguras** (https) siempre
- **Folder específico**: "elrincondelharco"
- **Validación de tipos**: Imágenes y PDFs aceptados
- **Nombres de archivo limpios**: Remueve caracteres especiales para URLs amigables
- **Forzado de descarga para PDFs**: URLs con `fl_attachment` para descarga automática
- **Manejo de archivos vacíos**: Validación y errores descriptivos

### Base de Datos (`app/db/session.py`)
- **AsyncEngine** con psycopg 3
- `pool_pre_ping=True` para conexiones estables
- `AsyncSession` con `expire_on_commit=False`
- **Pool size optimizado** para producción

### Seed de Datos (`app/db/seed.py`)
- **Script completo** para poblar todas las tablas
- **Datos reales** extraídos del frontend
- **DELETE + INSERT** para limpieza total
- **6 dominios poblados**: heroes (1), abouts (1), passions (1), projects (3), stacks (24), footers (1)
- **Comando disponible**: `pnpm seed`
- **Logs informativos** durante el proceso

### Modelos (`app/models/`)
- **Base declarativa** con imports automáticos
- Modelo **Example** con timestamps
- **7 dominios de portfolio** implementados:
  - **Hero**: Sección principal (title, subtitle, description, buttons, image_url, cv_url)
  - **About**: Información personal (experience, leadership, location, image_url)
  - **Passions**: Pasiones personales (family, games, coding, image_url)
  - **Projects**: Portafolio (tags, URLs, iconos, image_url)
  - **Stack**: Tecnologías (estilos flexibles, iconos, colores)
  - **Footer**: Contacto y enlaces (social media, quick_links JSONB)
  - **SiteSettings**: Configuración del sitio (brand, legal, social networks JSONB)
- **Tipos de datos optimizados**: String, Text, JSONB, Boolean

### API (`app/api/`)
- Router principal con **include_router**
- Endpoints **v1** organizados por dominio
- **Ejemplo funcional** con CRUD básico
- **7 dominios completos** con CRUD completo:
  - `GET /api/v1/{dominios}/` - Listar todos
  - `GET /api/v1/{dominios}/{id}` - Obtener por ID
  - `GET /api/v1/{dominios}/latest/` - Último registro (hero, about, passions, footer, site-settings)
  - `POST /api/v1/{dominios}/` - Crear (con upload de imagen/PDF)
  - `PUT /api/v1/{dominios}/{id}` - Actualizar (con upload de imagen/PDF)
  - `DELETE /api/v1/{dominios}/{id}` - Eliminar
- **Upload de imágenes y PDFs** integrado con Cloudinary
- **Form data handling** para todos los endpoints
- **CORS middleware** configurado para frontend

### Lifespan (`app/main.py`)
- Logs con emojis informativos
- Verificación de conexión a Neon
- Creación automática de tablas
- Timezone configurado (Europe/Madrid)
- **CORS middleware** inicializado
- **Health check** mejorado

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

# Frontend URL (para CORS)
FRONTEND_URL=http://localhost:4321
```

## 🐳 Docker

- **Python 3.12 slim** como base
- **Poetry** para gestión de dependencias
- **Usuario no-root** para seguridad
- **Health check** automático
- **Exposición puerto 8000**
- **Variables de entorno** desde Docker secrets

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
- **7 dominios de portfolio implementados**
- **CRUD completo para todos los dominios**
- **Upload de imágenes funcionando**
- **Schemas Pydantic completos**
- **Modelos SQLAlchemy optimizados**
- **Seed de datos inicial completado**
- **7 dominios poblados con datos reales del frontend**
- **CORS middleware configurado**
- **Panel admin frontend integrado**
- **Sistema de sincronización implementado**
- **SiteSettings para configuración de marca**

### ✅ Panel Admin Integration
- **Frontend completo** con 6 editores + Footer component
- **Sincronización en tiempo real** entre admin y público
- **Upload de imágenes y PDFs** mejorado con drag & drop
- **Form data handling** optimizado
- **Eventos personalizados** para actualización automática
- **PDF download automático** con nombres limpios
- **Footer component** con datos dinámicos desde backend

### ⚠️ Pendientes
- Configurar variables `.env` con API keys de Cloudinary
- Implementar autenticación JWT (opcional para portfolio)
- Tests unitarios completos
- Optimización de queries para producción
- Migrar componentes a Svelte 5 cuando lucide-svelte sea compatible

## 🚀 Próximos Pasos

1. **Configurar `.env`** con credenciales Neon y Cloudinary
2. **Ejecutar `pnpm dev`** para iniciar servidor
3. **Verificar conexión** y creación de tablas
4. **Probar endpoints** en `http://localhost:8000/docs`
5. **Ejecutar `pnpm seed`** para poblar datos iniciales
6. **Iniciar frontend** en `http://localhost:4321`
7. **Acceder al panel admin** en `http://localhost:4321/admin`
8. **Probar sincronización** entre admin y componentes públicos

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
- `POST /api/v1/heroes/` - Crear (con imagen y PDF)
- `PUT /api/v1/heroes/{id}` - Actualizar (con imagen y PDF)
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
- `PUT /api/v1/footers/{id}` - Actualizar (FormData)
- `DELETE /api/v1/footers/{id}` - Eliminar

#### SiteSettings (`/api/v1/site-settings/`)
- `GET /api/v1/site-settings/` - Listar todos
- `GET /api/v1/site-settings/{id}` - Obtener por ID
- `GET /api/v1/site-settings/latest/` - Último registro activo
- `POST /api/v1/site-settings/` - Crear (FormData)
- `PUT /api/v1/site-settings/{id}` - Actualizar (FormData)
- `DELETE /api/v1/site-settings/{id}` - Eliminar

### Example (Legacy)
- `GET /api/v1/example/` - Listar examples
- `POST /api/v1/example/` - Crear example
- `GET /api/v1/example/health` - Health check de ejemplo

## 🔗 Mapa de imports — fuente de verdad
| Qué importar       | Desde dónde                      |
|--------------------|----------------------------------|
| `get_db`           | `app.db.session`                 |
| `AsyncSession`     | `sqlalchemy.ext.asyncio`         |
| `Base`             | `app.models.base`                |
| `upload_image`     | `app.core.cloudinary`            |
| `settings`         | `app.core.config`                |

## 📡 Endpoints registrados actualmente
| Dominio      | Prefix               | GET latest | FormData |
|--------------|----------------------|------------|-----------|
| hero         | /api/v1/heroes       | sí         | sí        |
| about        | /api/v1/abouts       | sí         | sí        |
| stack        | /api/v1/stacks       | no         | no        |
| project      | /api/v1/projects     | no         | sí        |
| passion      | /api/v1/passions     | sí         | sí        |
| footer       | /api/v1/footers      | sí         | sí        |
| site-settings| /api/v1/site-settings| sí         | sí        |

---

## 🎯 **Panel Admin - Integración Completa**

### **Frontend Integration**
- ✅ **6 editores** conectados a los endpoints
- ✅ **Upload de imágenes** con Cloudinary
- ✅ **Form data** para todos los endpoints
- ✅ **Sincronización automática** con componentes públicos
- ✅ **Eventos personalizados** para actualización en tiempo real

### **Data Flow**
```
Panel Admin → FormData → API Backend → Neon PostgreSQL
     ↓
Eventos → Componentes Públicos → Recarga Automática
```

### **Características Técnicas**
- **FormData handling**: Todos los endpoints usan multipart/form-data
- **Upload de imágenes y PDFs**: Integración directa con Cloudinary
- **PDF download automático**: URLs con `fl_attachment` para descarga forzada
- **JSON fields**: Footer usa JSONB para quick_links
- **CORS**: Configurado para localhost:4321
- **Async operations**: Todas las operaciones son asíncronas

---

**Status**: 🟢 **PRODUCCIÓN LISTA**  
**Última Actualización**: Marzo 2026  
**Versión**: 2.2.0 (con Panel Admin, Sincronización, SiteSettings y PDF Upload)
