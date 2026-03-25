# 📋 Reglas de Orquestación del Proyecto

## 🎯 Propósito
Este archivo sirve como orquestador central para guiar las interacciones con el proyecto, asegurando que se consulten las referencias correctas y se mantenga la coherencia entre frontend, backend, Docker y testing.

## 📁 Estructura del Proyecto

### Frontend
- **Ubicación**: `/frontend/`
- **Documentación**: `.windsurf/frontend.md`
- **Tecnologías**: Svelte 5, TypeScript, TailwindCSS, Astro
- **Estado**: Componentes principales, estructura base

### Backend  
- **Ubicación**: `/backend/`
- **Documentación**: `.windsurf/backend.md`
- **Tecnologías**: FastAPI, PostgreSQL (Neon), psycopg 3, Poetry
- **Estado**: API funcional, configuración segura lista

### Docker & Despliegue
- **Ubicación**: `/backend/`, `/frontend/`
- **Documentación**: `.windsurf/docker.md`
- **Tecnologías**: Docker, Docker Compose, Nginx, Multi-stage builds
- **Estado**: Contenedores independientes, production ready

### Testing
- **Ubicación**: `/backend/tests/`
- **Documentación**: `.windsurf/test.md`
- **Tecnologías**: pytest, pytest-asyncio, httpx, coverage
- **Estado**: Suite completa 80%+ coverage

## 🔍 Reglas de Consulta

### 1. Consultas Específicas de Backend
- **Siempre consultar**: `.windsurf/backend.md` primero
- **Contexto**: Estructura de carpetas, endpoints, configuración
- **Archivos relevantes**: `backend/app/`, `backend/pyproject.toml`, `backend/scripts/`

### 2. Consultas Específicas de Frontend
- **Siempre consultar**: `.windsurf/frontend.md` primero  
- **Contexto**: Componentes Svelte 5, estilos, configuración
- **Archivos relevantes**: `frontend/src/`, `frontend/tailwind.config.js`

### 3. Consultas de Docker
- **Siempre consultar**: `.windsurf/docker.md` primero
- **Contexto**: Contenedores, builds, despliegue, variables de entorno
- **Archivos relevantes**: `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml`

### 4. Consultas de Testing
- **Siempre consultar**: `.windsurf/test-backend.md` primero
- **Contexto**: Tests unitarios, integración, coverage, fixtures
- **Archivos relevantes**: `backend/tests/`, `pytest.ini`, `scripts/run-tests.sh`

### 5. Consultas Integradas (Frontend + Backend)
- **Consultar ambos**: `.windsurf/backend.md` y `.windsurf/frontend.md`
- **Contexto**: Conexión API, tipos compartidos, flujo de datos
- **Puntos de integración**:
  - API endpoints (`/api/*`)
  - Tipos TypeScript vs Pydantic schemas
  - Autenticación y manejo de errores
  - Variables de entorno compartidas

### 6. Consultas de Despliegue
- **Consultar**: `.windsurf/docker.md` y documentación específica
- **Contexto**: Docker compose, scripts de setup, producción
- **Puntos clave**: Scripts, variables de entorno, health checks

## 🔄 Flujo de Trabajo

### Desarrollo Backend
1. Revisar `.windsurf/backend.md` para estructura actual
2. Modificar archivos en `/backend/app/`
3. **Ejecutar tests**: `./scripts/run-tests.sh unit`
4. Actualizar documentación si hay cambios estructurales
5. Verificar compatibilidad con endpoints del frontend

### Desarrollo Frontend  
1. Revisar `.windsurf/frontend.md` para componentes existentes
2. Modificar archivos en `/frontend/src/`
3. Verificar compatibilidad con backend
4. Actualizar documentación si se agregan componentes

### Docker y Despliegue
1. Revisar `.windsurf/docker.md` para configuración actual
2. Modificar Dockerfiles o docker-compose.yml
3. **Probar localmente**: `./scripts/setup.sh dev`
4. Actualizar documentación de cambios
5. **Verificar producción**: `./scripts/setup.sh prod`

### Testing
1. Revisar `.windsurf/test.md` para estrategia de tests
2. Agregar nuevos tests en `/backend/tests/`
3. **Ejecutar suite**: `./scripts/run-tests.sh all`
4. Verificar coverage (80%+ mínimo)
5. Actualizar documentación si se agregan nuevos tipos de tests

### Desarrollo Integrado
1. **Primero**: Consultar `.windsurf/backend.md`, `.windsurf/frontend.md`, `.windsurf/docker.md`
2. **Después**: Identificar puntos de conexión necesarios
3. **Luego**: Implementar cambios coordinados
4. **Testing**: Ejecutar tests relevantes de ambos lados
5. **Finalmente**: Actualizar todas las documentaciones afectadas

## 📋 Checklist Antes de Modificar

### Para Backend
- [ ] He leído `.windsurf/backend.md`
- [ ] Conozco la estructura actual de endpoints
- [ ] Verifico impacto en frontend
- [ ] **Ejecuté tests**: `./scripts/run-tests.sh unit`
- [ ] Actualizo la documentación si es necesario

### Para Frontend
- [ ] He leído `.windsurf/frontend.md`
- [ ] Conozco los componentes existentes
- [ ] Verifico compatibilidad con backend
- [ ] Actualizo la documentación si es necesario

### Para Docker
- [ ] He leído `.windsurf/docker.md`
- [ ] Conozco la estructura actual de contenedores
- [ ] Verifico variables de entorno necesarias
- [ ] **Probé localmente**: `./scripts/setup.sh dev`
- [ ] Actualizo la documentación si es necesario

### Para Testing
- [ ] He leído `.windsurf/test.md`
- [ ] Conozco la estrategia de tests actual
- [ ] Agrego tests para nueva funcionalidad
- [ ] **Verifico coverage**: `./scripts/run-tests.sh coverage`
- [ ] Actualizo la documentación si es necesario

### Para Integración
- [ ] He leído todas las documentaciones relevantes
- [ ] Identifiqué los puntos de conexión
- [ ] Verifico tipos y formatos de datos
- [ ] **Ejecuté tests integrales**: `./scripts/run-tests.sh integration`
- [ ] Actualizo todas las documentaciones afectadas

## 🎯 Preguntas Guía

### Sobre Backend
- "¿Cuál es la estructura actual de la API?"
- "¿Qué endpoints están disponibles?"
- "¿Cómo está configurada la conexión a la base de datos?"
- "¿Qué modelos y schemas existen?"
- "¿Qué tests cubren la funcionalidad?"

### Sobre Frontend
- "¿Qué componentes Svelte 5 están disponibles?"
- "¿Cómo está configurado TailwindCSS?"
- "¿Qué estructura de carpetas sigue el frontend?"
- "¿Qué tipos TypeScript están definidos?"

### Sobre Docker
- "¿Cómo están configurados los contenedores?"
- "¿Qué variables de entorno necesita cada servicio?"
- "¿Cómo se ejecutan los scripts de setup?"
- "¿Cuál es el flujo de despliegue?"

### Sobre Testing
- "¿Qué tipo de tests están implementados?"
- "¿Cómo ejecuto la suite de tests?"
- "¿Cuál es el coverage actual?"
- "¿Cómo agrego nuevos tests?"

### Sobre Integración
- "¿Cómo se conecta el frontend con la API?"
- "¿Qué endpoints consume el frontend?"
- "¿Cómo se manejan los errores entre frontend y backend?"
- "¿Qué tipos de datos se comparten?"
- "¿Cómo se despliega todo junto?"

## 🚨 Reglas Importantes

1. **NUNCA modificar sin consultar primero la documentación relevante**
2. **SIEMPRE actualizar la documentación después de cambios estructurales**
3. **VERIFICAR compatibilidad entre frontend y backend**
4. **MANTENER coherencia en nombres y formatos**
5. **DOCUMENTAR nuevos endpoints y componentes**
6. **EJECUTAR tests antes y después de cambios importantes**
7. **PROBAR configuración Docker en desarrollo antes de producción**
8. **MANTENER coverage de tests >= 80%**

## 📞 Comandos Rápidos

### Backend
```bash
cd backend
poetry install          # Instalar dependencias
poetry run uvicorn app.main:app --reload --host 0.0.0.0  # Desarrollo
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000    # Producción
```

### Testing
```bash
cd backend
./scripts/run-tests.sh          # Todos los tests
./scripts/run-tests.sh unit      # Solo unit tests
./scripts/run-tests.sh integration # Integration tests
./scripts/run-tests.sh coverage  # Con coverage report
```

### Frontend
```bash
cd frontend  
pnpm install         # Instalar dependencias
pnpm run dev       # Iniciar servidor de desarrollo
pnpm run build     # Construir para producción
```

### Docker
```bash
# Backend
cd backend
./scripts/setup.sh dev    # Desarrollo con Docker
./scripts/setup.sh prod   # Producción con Docker
./scripts/setup.sh stop   # Detener servicios
./scripts/setup.sh logs   # Ver logs

# Frontend (si aplica)
cd frontend
./setup.sh build      # Construir imagen
./setup.sh up         # Iniciar contenedor
./setup.sh stop       # Detener contenedor
```

### Flujo Completo de Desarrollo

1. **Configurar Variables de Entorno**
   ```bash
   # Backend
   cd backend
   ./scripts/poetry-setup.sh
   
   # Editar .env con credenciales reales
   ```

2. **Iniciar Desarrollo Local**
   ```bash
   # Backend (sin Docker)
   cd backend
   poetry run uvicorn app.main:app --reload
   
   # Frontend
   cd frontend
   pnpm run dev
   ```

3. **Ejecutar Tests**
   ```bash
   cd backend
   ./scripts/run-tests.sh all
   ```

4. **Probar con Docker**
   ```bash
   cd backend
   ./scripts/setup.sh dev
   ```

5. **Verificar Funcionamiento**
   - Frontend: http://localhost:4321
   - Backend API: http://localhost:8000/docs
   - Health Checks: http://localhost:8000/health

6. **Desplegar en Producción**
   ```bash
   cd backend
   ./scripts/setup.sh prod
   ```

7. **Monitoreo y Logs**
   ```bash
   ./scripts/setup.sh logs      # Ver logs
   ./scripts/setup.sh status    # Ver estado
   ```

---

## 📚 Referencias Rápidas

### Archivos de Documentación
- **`.windsurf/backend.md`** - Estructura y configuración del backend
- **`.windsurf/frontend.md`** - Componentes y configuración del frontend
- **`.windsurf/docker.md`** - Configuración de Docker y despliegue
- **`.windsurf/test-backend.md`** - Estrategia y ejecución de tests backend
- **`.windsurf/test-frontend.md`** - Estrategia y ejecución de tests frontend
- **`.windsurf/rules.md`** - Este archivo (orquestación central)

### Scripts Importantes
- **`backend/scripts/setup.sh`** - Gestión Docker del backend
- **`backend/scripts/run-tests.sh`** - Ejecución de tests backend
- **`backend/scripts/poetry-setup.sh`** - Configuración del entorno backend
- **`backend/scripts/seed-db.sh`** - Poblado de base de datos
- **`frontend/scripts/run-tests.sh`** - Ejecución de tests frontend

### Comandos Esenciales
```bash
# Desarrollo completo
cd backend && ./scripts/setup.sh dev &
cd frontend && pnpm run dev

# Tests completos
cd backend && ./scripts/run-tests.sh coverage
cd frontend && ./scripts/run-tests.sh coverage

# Tests específicos
cd backend && ./scripts/run-tests.sh unit
cd frontend && ./scripts/run-tests.sh unit

# Producción
cd backend && ./scripts/setup.sh prod
```

**Nota**: Este archivo es la primera referencia ante cualquier duda sobre la estructura o estado del proyecto. Siempre consulta aquí primero para saber qué documentación específica leer.
