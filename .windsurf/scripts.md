# Scripts del Backend - Portfolio elRincondeHarco

## 📋 Descripción General

La carpeta `backend/scripts/` contiene scripts de automatización para facilitar el desarrollo, despliegue y mantenimiento del backend FastAPI.

## 🗂️ Lista de Scripts

### 1. **setup.sh** - Gestión Docker del Backend
**Propósito**: Orquestar los servicios Docker del backend (aplicación + base de datos)

#### **Uso**
```bash
./scripts/setup.sh [prod|stop|logs|status]
```

#### **Comandos Disponibles**
- **`prod`**: Inicia backend + DB en modo producción
- **`stop`**: Detiene todos los servicios
- **`logs`**: Muestra logs en tiempo real
- **`status`**: Muestra estado de los contenedores

#### **Funcionalidades**
- Detección automática de `docker compose` vs `docker-compose`
- Verificación de archivo `.env` antes de iniciar
- Monitoreo de estabilidad de contenedores
- Logging con colores y mensajes informativos

#### **Ejemplo de Uso**
```bash
# Iniciar producción
./scripts/setup.sh prod

# Ver logs
./scripts/setup.sh logs

# Detener servicios
./scripts/setup.sh stop
```

---

### 2. **poetry-setup.sh** - Configuración del Entorno Poetry
**Propósito**: Configurar el entorno de desarrollo Python con Poetry

#### **Uso**
```bash
./scripts/poetry-setup.sh [development|production]
```

#### **Funcionalidades**
- Verificación de instalación de Poetry
- Validación de versión de Python (3.12+ recomendado)
- Instalación de dependencias según entorno
- Creación automática de archivo `.env` template
- Validación de configuración inicial

#### **Variables de Entorno Creadas**
- Configuración PostgreSQL local
- URL de base de datos auto-generada
- Settings de aplicación (DEBUG, SECRET_KEY)
- Configuración Cloudinary
- URL del frontend

#### **Ejemplo de Uso**
```bash
# Setup desarrollo
./scripts/poetry-setup.sh development

# Setup producción
./scripts/poetry-setup.sh production
```

---

### 3. **run-tests.sh** - Ejecución de Tests
**Propósito**: Ejecutar la suite de tests del backend con diferentes opciones

#### **Uso**
```bash
./scripts/run-tests.sh [unit|integration|all|coverage|fast]
```

#### **Tipos de Tests**
- **`unit`**: Tests unitarios (models, CRUD, config)
- **`integration`**: Tests de integración (API, database)
- **`all`**: Todos los tests
- **`coverage`**: Tests con reporte de cobertura
- **`fast`**: Tests rápidos (excluye marcados como slow)

#### **Funcionalidades**
- Instalación automática de dependencias de testing
- Ejecución con pytest y opciones específicas
- Generación de reportes de cobertura HTML
- Filtrado por categorías de tests

#### **Ejemplo de Uso**
```bash
# Ejecutar todos los tests
./scripts/run-tests.sh all

# Ver cobertura
./scripts/run-tests.sh coverage

# Tests rápidos durante desarrollo
./scripts/run-tests.sh fast
```

---

### 4. **seed-db.sh** - Poblado de Base de Datos
**Propósito**: Poblar la base de datos con datos iniciales de ejemplo

#### **Uso**
```bash
./scripts/seed-db.sh
```

#### **Funcionalidades**
- Verificación de archivo `.env`
- Espera activa de disponibilidad de la base de datos
- Ejecución del script de seed (`app.db.seed`)
- Manejo de errores con logging informativo

#### **Proceso**
1. Carga variables desde `.env`
2. Espera a que PostgreSQL esté listo
3. Ejecuta el módulo `app.db.seed`
4. Confirma éxito del proceso

#### **Ejemplo de Uso**
```bash
# Poblar base de datos
./scripts/seed-db.sh
```

---

### 5. **entrypoint.sh** - Entrypoint de Docker
**Propósito**: Script de inicialización para contenedores Docker

#### **Uso**
```bash
# Se ejecuta automáticamente en Docker containers
# No requiere ejecución manual
```

#### **Funcionalidades**
- **Verificación de conexión**: Espera a que la DB esté disponible
- **Creación de schema**: Asegura que el schema PostgreSQL exista
- **Migraciones**: Ejecuta migraciones de Alembic
- **Inicio de aplicación**: Lanza el servidor Uvicorn

#### **Proceso de Inicialización**
1. **Conexión DB**: Espera hasta 30 segundos por conexión
2. **Schema**: Crea schema si no existe
3. **Migraciones**: Aplica migraciones pendientes
4. **Servidor**: Inicia aplicación en `host 0.0.0.0:8000`

#### **Manejo de Errores**
- Timeout en conexión a base de datos
- Manejo de errores en migraciones (no crítico)
- Logging detallado de cada paso

---

## 🔄 Flujo de Trabajo Recomendado

### **Primera Vez (Setup Local)**
```bash
# 1. Configurar entorno Poetry
./scripts/poetry-setup.sh development

# 2. Actualizar .env con credenciales locales
vim .env

# 3. Iniciar con Docker
./scripts/setup.sh prod

# 4. Poblar base de datos
./scripts/seed-db.sh

# 5. Ejecutar tests
./scripts/run-tests.sh coverage
```

### **Desarrollo Diario**
```bash
# Iniciar servicios
./scripts/setup.sh prod

# Ver logs
./scripts/setup.sh logs

# Ejecutar tests rápidos
./scripts/run-tests.sh fast
```

### **Despliegue Producción**
```bash
# Setup producción
./scripts/poetry-setup.sh production

# Iniciar servicios
./scripts/setup.sh prod

# Verificar estado
./scripts/setup.sh status
```

## 🛠️ Características Técnicas

### **Manejo de Errores**
- Todos los scripts usan `set -e` para detener en errores
- Logging con colores y mensajes claros
- Verificación de prerequisitos antes de ejecutar

### **Compatibilidad**
- Soporte para `docker compose` y `docker-compose`
- Detección automática de comandos disponibles
- Compatible con Linux y macOS

### **Configuración**
- Uso de variables de entorno desde `.env`
- Templates automáticos para configuración
- Validación de dependencias y versiones

## 📝 Notas Importantes

1. **Permisos**: Asegurar que los scripts sean ejecutables:
   ```bash
   chmod +x backend/scripts/*.sh
   ```

2. **Environment**: El archivo `.env` debe existir antes de usar Docker

3. **Python**: Se recomienda Python 3.12+ para mejor compatibilidad

4. **Poetry**: Debe estar instalado para usar `poetry-setup.sh`

5. **Docker**: Requiere Docker y Docker Compose instalados

---

*Documentación actualizada: Marzo 2026 - Estado: Scripts Production Ready*
