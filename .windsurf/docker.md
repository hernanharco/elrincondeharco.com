# Docker - Portfolio elRincondeHarco

## 📋 Resumen de Implementación

### 🎯 **Objetivo**
Dockerizar la aplicación portfolio completa (frontend + backend) para producción y facilitar el despliegue en plataformas como Render y Vercel.

### 🏗️ **Arquitectura Actual**

#### **Frontend (Astro 6 + Svelte 5)**
- **Imagen**: `portfolioelrincondeharcocom-frontend`
- **Puerto**: 4321
- **Base**: Node.js 22 Alpine (builder) + Nginx Alpine (production)
- **Estrategia**: Multi-stage build optimizado
- **Servidor**: Nginx con configuración personalizada
- **Gestor de paquetes**: pnpm
- **Build output**: Sitio estático servido por Nginx

#### **Backend (FastAPI + PostgreSQL)**
- **Imagen**: `portfolioelrincondeharcocom-backend`
- **Puerto**: 8000
- **Base**: Python 3.12 Slim
- **Gestión**: Poetry para dependencias
- **Servidor**: Uvicorn
- **Base de datos**: PostgreSQL 16 Alpine (local) + Neon (producción)

#### **Base de Datos (PostgreSQL)**
- **Imagen**: `postgres:16-alpine`
- **Puerto**: 5432
- **Usuario**: neondb_owner
- **Base de datos**: neondb
- **Persistencia**: Volumen Docker `postgres_data`
- **Health check**: `pg_isready` integrado

### 📁 **Estructura de Archivos Actual**

```
Portfolio/
├── docker-compose.yml          # Orquestación de 3 servicios (db + frontend + backend)
├── setup.sh                    # Script de gestión mejorado (198 líneas)
├── seed-db.sh                  # Script especializado para seed de BD (136 líneas)
├── frontend/
│   ├── Dockerfile             # Multi-stage: Node.js builder + Nginx production
│   ├── nginx.conf             # Configuración Nginx personalizada
│   ├── package.json           # Astro 6.0.6 + Svelte 5.54.0
│   ├── pnpm-lock.yaml         # Lockfile de dependencias
│   ├── .env                  # Variables entorno frontend
│   └── .dockerignore         # Excluir node_modules y .astro
├── backend/
│   ├── Dockerfile             # Python 3.12 + Poetry + migraciones Alembic
│   ├── pyproject.toml        # FastAPI 0.104.1 + dependencias
│   ├── poetry.lock           # Lockfile de Poetry
│   ├── .env.local            # Configuración BD local (Docker)
│   ├── .env.production       # Configuración BD Neon (producción)
│   ├── app/db/seed.py        # Script de seed mejorado
│   └── .dockerignore         # Excluir .venv y __pycache__
└── .windsurf/
    └── docker.md            # Este archivo
```

### 🔧 **Configuración Técnica Actual**

#### **Frontend Dockerfile (Multi-stage):**
```dockerfile
# Stage 1: Builder
FROM node:22-alpine AS builder
ARG PUBLIC_API_URL
RUN npm install -g pnpm
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

# Stage 2: Production
FROM nginx:alpine AS production
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 4321
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["wget", "-qO-", "http://localhost:4321/"]
CMD ["nginx", "-g", "daemon off;"]
```

#### **Backend Dockerfile (Actualizado):**
```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root
COPY app/ ./app/
# Copiar migraciones y configuración de Alembic
COPY migrations/ ./migrations/
COPY alembic.ini ./alembic.ini
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["curl", "-f", "http://localhost:8000/docs"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **Base de Datos Dockerfile:**
```dockerfile
# Imagen oficial postgres:16-alpine
env_file:
  - ./backend/.env
environment:
  POSTGRES_DB: ${PGDATABASE:-neondb}
  POSTGRES_USER: ${PGUSER:-neondb_owner}
  POSTGRES_PASSWORD: ${PGPASSWORD:-localpassword}
ports:
  - "5432:5432"
volumes:
  - postgres_data:/var/lib/postgresql/data
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${PGUSER:-neondb_owner} -d ${PGDATABASE:-neondb}"]
```

#### **Nginx Config:**
- **Puerto**: 4321
- **Compresión gzip**: Activada
- **Caché estática**: 1 año para assets con hash
- **Routing**: SPA fallback a index.html

### 🚀 **Comandos de Uso**

#### **Script Principal (setup.sh - Actualizado):**
```bash
./setup.sh dev        # Desarrollo con Postgres local (Docker)
./setup.sh prod       # Producción simulada con Postgres local (Docker)
./setup.sh prod-neon  # Producción real con base de datos Neon
./setup.sh db-info    # Mostrar datos de conexión para DBeaver
./setup.sh stop       # Detener todos los servicios
./setup.sh clean      # Limpiar contenedores y volúmenes
./setup.sh logs       # Mostrar logs de los servicios
./setup.sh status     # Ver estado de los servicios
./setup.sh help       # Mostrar esta ayuda
```

#### **Script de Seed (seed-db.sh - 136 líneas):**
```bash
./seed-db.sh          # Ejecutar seed de base de datos
# Características:
# - Carga variables desde .env automáticamente
# - Espera a que PostgreSQL esté listo
# - Ejecuta seed dentro del contenedor backend
# - Manejo de errores y reintentos
```

#### **Docker Compose Directo:**
```bash
docker-compose up --build -d    # Construir e iniciar producción
docker-compose up --build       # Construir e iniciar desarrollo
docker-compose down              # Detener y remover contenedores
docker-compose logs -f           # Logs en tiempo real
docker-compose ps                # Estado de servicios
```

### 🌐 **Acceso a Servicios**

#### **Producción Local:**
- **Frontend**: http://localhost:4321/
- **Backend API**: http://localhost:8000/docs
- **Base de Datos**: localhost:5432 (PostgreSQL local)
- **Health Checks**: Configurados para los 3 servicios

#### **Conexión a Base de Datos (DBeaver):**
```
Host: localhost
Port: 5432
Database: neondb
Username: neondb_owner
Password: localpassword
SSL: desactivado
URL: postgresql://neondb_owner:localpassword@localhost:5432/neondb
```

#### **Despliegue:**
- **Render**: Backend (FastAPI) con Neon PostgreSQL
- **Vercel**: Frontend (Static Site)
- **Docker Hub**: Imágenes listas para push

### 🔐 **Variables de Entorno**

#### **Frontend (.env) - Actual:**
```bash
NODE_ENV=production
FRONTEND_URL=http://localhost:4321
PUBLIC_API_URL=http://localhost:8000
```

#### **Backend (.env.local) - Base de Datos Local:**
```bash
PGHOST=db
PGDATABASE=neondb
PGUSER=neondb_owner
PGPASSWORD=localpassword
PGSSLMODE=disable
PGCHANNELBINDING=disable
DATABASE_URL=postgresql+psycopg://neondb_owner:localpassword@db/neondb
SECRET_KEY=portfolio-secret-key-2024
CLOUDINARY_CLOUD_NAME=dxyk76jhu
CLOUDINARY_API_KEY=897545319274682
CLOUDINARY_API_SECRET=eWQ_l3-fJG6G5eV8TfNfz_15Tws
FRONTEND_URL=http://localhost:4321
```

#### **Backend (.env.production) - Base de Datos Neon:**
```bash
PGHOST="your-neon-host"
PGDATABASE="neondb"
PGUSER="neondb_owner"
PGPASSWORD="your-password"
PGSSLMODE="require"
PGCHANNELBINDING="require"
DATABASE_URL=postgresql+psycopg://${PGUSER}:${PGPASSWORD}@${PGHOST}/${PGDATABASE}?sslmode=require&channel_binding=require
SECRET_KEY="your-secret-key-change-me"
CLOUDINARY_CLOUD_NAME="dxyk76jhu"
CLOUDINARY_API_KEY="your-api-key-change-me"
CLOUDINARY_API_SECRET="your-api-secret-change-me"
FRONTEND_URL="http://localhost:4321"
```

#### **Gestión Automática:**
- El script `setup.sh` selecciona automáticamente el archivo .env adecuado
- `dev` y `prod` usan `.env.local` (PostgreSQL local)
- `prod-neon` usa `.env.production` (Neon cloud)

### 📊 **Estado Actual del Proyecto**

#### **✅ Funcionalidades Implementadas:**
- [x] **Frontend**: Astro 6.0.6 + Svelte 5.54.0 con @iconify/svelte
- [x] **Backend**: FastAPI 0.104.1 + PostgreSQL (local + Neon)
- [x] **Base de Datos**: PostgreSQL 16 Alpine con persistencia
- [x] **Docker**: Multi-stage build optimizado para 3 servicios
- [x] **Nginx**: Configuración personalizada con gzip y caché
- [x] **Health Checks**: Para los 3 servicios (frontend, backend, db)
- [x] **Script setup.sh**: 198 líneas con gestión completa
- [x] **Script seed-db.sh**: 136 líneas especializado en seed
- [x] **Variables de entorno**: Separadas por entorno (local/prod)
- [x] **Poetry**: Gestión de dependencias Python
- [x] **pnpm**: Gestión de dependencias Node.js
- [x] **Alembic**: Migraciones de base de datos integradas
- [x] **Usuario no-root**: Seguridad en contenedor backend
- [x] **Seed de datos**: Script mejorado con fix Cloudinary PDF

#### **🔧 Versiones Actuales:**
- **Node.js**: 22.12.0+ (requerido por Astro)
- **Python**: 3.12
- **PostgreSQL**: 16 Alpine
- **Astro**: 6.0.6
- **Svelte**: 5.54.0
- **FastAPI**: 0.104.1
- **Poetry**: Latest
- **pnpm**: Latest

#### **🌐 Características Técnicas:**
- **Frontend**: Sitio estático optimizado con Nginx
- **Backend**: API REST con documentación Swagger
- **Base de datos**: Dual (PostgreSQL local + Neon cloud)
- **Storage**: Cloudinary integrado
- **Security**: Usuario no-root, variables de entorno separadas
- **Performance**: Compresión gzip, caché de 1 año para assets
- **Development**: Flujo completo local con Docker
- **Production**: Deploy ready con múltiples opciones

### 🎯 **Roadmap de Mejoras**

#### **🚀 Mejoras Inmediatas:**
1. **Testing**: Unit tests para backend y E2E tests para frontend
2. **CI/CD**: GitHub Actions para build y deploy automático
3. **Monitoring**: Logs estructurados y métricas con Prometheus
4. **Security**: Escaneo de vulnerabilidades con Snyk/Trivy
5. **Performance**: Image optimization y lazy loading

#### **🔮 Mejoras a Largo Plazo:**
1. **Microservicios**: Separar funcionalidades específicas
2. **CDN**: CloudFlare para distribución global
3. **Caching**: Redis para sesiones y caché de API
4. **Analytics**: Google Analytics o alternativa privacy-first
5. **PWA**: Progressive Web App capabilities

### 🏆 **Resumen de Implementación**

**Dockerización completada con arquitectura enterprise-ready:**
- ✅ **Frontend**: Astro 6 + Svelte 5 + Nginx (multi-stage)
- ✅ **Backend**: FastAPI + Python 3.12 + Poetry + Alembic
- ✅ **Base de datos**: PostgreSQL 16 local + Neon cloud
- ✅ **Storage**: Cloudinary para media
- ✅ **Scripting**: setup.sh (198 líneas) + seed-db.sh (136 líneas)
- ✅ **Security**: Best practices, usuario no-root, .env separados
- ✅ **Performance**: Nginx optimizado, gzip, caché
- ✅ **Development**: Flujo completo local con Docker
- ✅ **Production**: Multi-environment ready
- ✅ **Data**: Seed automático con manejo de errores
- ✅ **Monitoring**: Health checks para todos los servicios
- ✅ **Listo para deploy** 🚀

---

*Documentación actualizada: Marzo 2026 - Estado: Enterprise Production Ready*
