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

### 📁 **Estructura de Archivos Docker Actual**

```
Portfolio/
├── backend/
│   ├── docker-compose.yml       # Orquestación backend (conecta a Neon)
│   ├── scripts/setup.sh          # Script de gestión backend (49 líneas)
│   ├── scripts/seed-db.sh        # Script especializado para seed (41 líneas)
│   ├── scripts/entrypoint.sh     # Entrypoint para migraciones y schema
│   ├── Dockerfile               # Python 3.12 + Poetry + libpq-dev + entrypoint
│   ├── pyproject.toml          # FastAPI + dependencias
│   ├── poetry.lock             # Lockfile de Poetry
│   ├── .env                    # Configuración Neon PostgreSQL
│   ├── app/db/seed.py          # Script de seed mejorado
│   └── .dockerignore           # Excluir .venv y __pycache__
├── frontend/
│   ├── setup.sh                # Script de gestión frontend (54 líneas)
│   ├── Dockerfile              # Multi-stage: Node.js builder + Nginx production
│   ├── nginx.conf              # Configuración Nginx personalizada
│   ├── package.json            # Astro 6.0.6 + Svelte 5.54.0
│   ├── pnpm-lock.yaml          # Lockfile de dependencias
│   ├── .env                   # Variables entorno frontend
│   └── .dockerignore          # Excluir node_modules y .astro
└── .windsurf/
    └── docker.md             # Este archivo
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
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini ./alembic.ini
COPY scripts/entrypoint.sh ./scripts/entrypoint.sh
RUN chmod +x ./scripts/entrypoint.sh
RUN sed -i 's/\r$//' ./scripts/entrypoint.sh
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["curl", "-f", "http://localhost:8000/docs"]
ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **Docker Compose (Backend Only):**
```yaml
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: elrincon-backend
    restart: always
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-production}
      - PGHOST=${PGHOST}
      - PGPORT=${PGPORT}
      - PGDATABASE=${PGDATABASE}
      - PGUSER=${PGUSER}
      - PGPASSWORD=${PGPASSWORD}
      - PGSCHEMA=${PGSCHEMA}
      - DATABASE_URL=${DATABASE_URL}
    env_file:
      - .env
    networks:
      - harco_network

networks:
  harco_network:
    name: harco_network
    external: true
```

#### **Nginx Config:**
- **Puerto**: 4321
- **Compresión gzip**: Activada
- **Caché estática**: 1 año para assets con hash
- **Routing**: SPA fallback a index.html

### 🚀 **Comandos de Uso**

#### **Backend Scripts:**
```bash
cd backend/
./scripts/setup.sh prod        # Iniciar backend en modo producción
./scripts/setup.sh stop        # Detener servicios backend
./scripts/setup.sh logs        # Ver logs de servicios backend
./scripts/setup.sh status      # Ver estado de servicios backend

./scripts/seed-db.sh           # Ejecutar seed de base de datos
# Características:
# - Carga variables desde .env automáticamente
# - Espera a que PostgreSQL esté listo
# - Ejecuta seed dentro del contenedor backend
# - Manejo de errores y reintentos
```

#### **Frontend Scripts:**
```bash
cd frontend/
./setup.sh build       # Construir imagen Docker
./setup.sh up          # Iniciar contenedor frontend
./setup.sh stop        # Detener contenedor frontend
./setup.sh logs        # Ver logs del frontend
```

#### **Docker Compose Directo:**
```bash
cd backend/
docker-compose up --build -d    # Construir e iniciar backend
docker-compose down              # Detener y remover contenedor
docker-compose logs -f           # Logs en tiempo real
docker-compose ps                # Estado de servicios
```

### 🌐 **Acceso a Servicios**

#### **Producción Local:**
- **Frontend**: http://localhost:4321/
- **Backend API**: http://localhost:8000/docs
- **Base de Datos**: Neon PostgreSQL (nube)
- **Health Checks**: Configurados para frontend y backend

#### **Conexión a Base de Datos (Neon):**
```
Host: tu-neon-host.neon.tech
Port: 5432
Database: neondb
Username: neondb_owner
Password: tu-password
SSL: requerido
URL: postgresql+psycopg://neondb_owner:tu-password@tu-neon-host.neon.tech/neondb?sslmode=require
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

#### **Backend (.env) - Neon PostgreSQL:**
```bash
PGHOST=tu-neon-host.neon.tech
PGDATABASE=neondb
PGUSER=neondb_owner
PGPASSWORD=tu-password
PGSSLMODE=require
PGCHANNELBINDING=require
DATABASE_URL=postgresql+psycopg://neondb_owner:tu-password@tu-neon-host.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=portfolio-secret-key-2024
CLOUDINARY_CLOUD_NAME=dxyk76jhu
CLOUDINARY_API_KEY=897545319274682
CLOUDINARY_API_SECRET=eWQ_l3-fJG6G5eV8TfNfz_15Tws
FRONTEND_URL=http://localhost:4321
```

### 📊 **Estado Actual del Proyecto**

#### **✅ Funcionalidades Docker Implementadas:**
- [x] **Frontend**: Astro 6.0.6 + Svelte 5.54.0 con @iconify/svelte
- [x] **Backend**: FastAPI + Python 3.12 + Poetry
- [x] **Base de Datos**: Neon PostgreSQL (nube) con Docker compose
- [x] **Docker**: Multi-stage build optimizado para frontend y backend
- [x] **Nginx**: Configuración personalizada con gzip y caché
- [x] **Health Checks**: Para frontend y backend
- [x] **Scripts separados**: Backend (scripts/setup.sh) + Frontend (setup.sh)
- [x] **Script seed-db.sh**: 41 líneas especializado en seed
- [x] **Variables de entorno**: Configuración para Neon PostgreSQL
- [x] **Poetry**: Gestión de dependencias Python
- [x] **pnpm**: Gestión de dependencias Node.js
- [x] **Alembic**: Migraciones de base de datos integradas
- [x] **Entrypoint**: Script para preparación de base de datos
- [x] **Usuario no-root**: Seguridad en contenedor backend
- [x] **Seed de datos**: Script mejorado con fix Cloudinary PDF

#### **🔧 Versiones Actuales:**
- **Node.js**: 22.12.0+ (requerido por Astro)
- **Python**: 3.12
- **PostgreSQL**: Neon PostgreSQL (nube)
- **Astro**: 6.0.6
- **Svelte**: 5.54.0
- **FastAPI**: Latest
- **Poetry**: Latest
- **pnpm**: Latest

#### **🌐 Características Docker:**
- **Frontend**: Sitio estático optimizado con Nginx
- **Backend**: API REST con documentación Swagger
- **Base de datos**: Neon PostgreSQL (nube) con Docker compose
- **Storage**: Cloudinary integrado
- **Security**: Usuario no-root, variables de entorno
- **Performance**: Compresión gzip, caché de 1 año para assets
- **Development**: Flujo completo local con Docker separado
- **Production**: Deploy ready con contenedores independientes

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

**Dockerización completada con arquitectura separada:**
- ✅ **Frontend**: Astro 6 + Svelte 5 + Nginx (multi-stage)
- ✅ **Backend**: FastAPI + Python 3.12 + Poetry + Alembic + Entrypoint
- ✅ **Base de datos**: Neon PostgreSQL (nube) con Docker compose
- ✅ **Storage**: Cloudinary para media
- ✅ **Scripting**: Backend scripts/setup.sh + Frontend setup.sh + scripts/seed-db.sh
- ✅ **Security**: Best practices, usuario no-root, variables de entorno
- ✅ **Performance**: Nginx optimizado, gzip, caché
- ✅ **Development**: Flujo completo local con Docker separado
- ✅ **Production**: Contenedores independientes ready
- ✅ **Data**: Seed automático con manejo de errores
- ✅ **Monitoring**: Health checks para frontend y backend
- ✅ **Arquitectura modular**: Frontend y backend independientes 🚀

---

*Documentación actualizada: Marzo 2026 - Estado: Docker Separado Production Ready*
