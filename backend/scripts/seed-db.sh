#!/bin/bash
# Eliminamos 'set -e' temporalmente para que el check no mate el script si falla
set +e

# Colores para un log profesional
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log()     { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# 1. Detección de Entorno
if [ -f "/.dockerenv" ]; then
    IN_DOCKER=true
    log "📦 Ejecutando dentro del contenedor (Modo Producción/Dokploy)"
else
    IN_DOCKER=false
    log "💻 Ejecutando desde máquina host (Modo Local)"
fi

# 2. Carga de variables (Solo si no estamos en Docker)
if [ "$IN_DOCKER" = false ]; then
    if [ -f ".env" ]; then
        log "📄 Cargando variables desde .env local..."
        set -a
        source <(grep -v '^#' .env | sed 's/\r$//')
        set +a
    else
        error "No se encontró el archivo .env en local"
    fi
fi

# 3. Intento de conexión informativa
log "⏳ Verificando disponibilidad de DB ($PGHOST:$PGPORT)..."
python3 -c "
import socket
try:
    with socket.create_connection(('$PGHOST', int('$PGPORT')), timeout=2):
        print('   ✅ Puerto abierto detectado.')
except:
    print('   ⚠️  Aviso: El puerto parece cerrado desde fuera, intentaremos conectar de todas formas...')
"

# Volvemos a activar set -e para que si falla el seed real, el script se detenga
set -e

# 4. Ejecutar el Seed
log "🚀 Ejecutando seed de base de datos..."

if [ "$IN_DOCKER" = true ]; then
    python -m app.db.seed
else
    if command -v poetry >/dev/null 2>&1; then
        log "🐍 Entorno local detectado: Usando Poetry..."
        # Si esto falla, aquí verás el error real de SQLAlchemy
        poetry run python -m app.db.seed
    else
        log "🐳 Usando Docker Compose como fallback..."
        docker compose exec -T backend python -m app.db.seed || error "Falló el seed vía Docker"
    fi
fi

success "✅ ¡Base de datos poblada con éxito!"