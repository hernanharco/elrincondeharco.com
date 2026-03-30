#!/bin/bash
set -e

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

# 2. Carga de variables (Solo si no estamos en Docker, ya que Docker ya las tiene)
if [ "$IN_DOCKER" = false ]; then
    if [ -f ".env" ]; then
        log "📄 Cargando variables desde .env local..."
        export $(grep -v '^#' .env | xargs)
    else
        error "No se encontró el archivo .env en local"
    fi
fi

# 3. Esperar a la DB de forma universal
log "⏳ Esperando a que la DB (${PGHOST:-localhost}) esté lista..."
python3 -c "
import socket
import time
import os
host = os.getenv('PGHOST', 'localhost')
port = int(os.getenv('PGPORT', 5432))
start = time.time()
while time.time() - start < 30:
    try:
        with socket.create_connection((host, port), timeout=1):
            exit(0)
    except:
        time.sleep(1)
exit(1)
" || error "No se pudo conectar a la DB en ${PGHOST}"

# 4. Ejecutar el Seed
log "🚀 Ejecutando seed de base de datos..."

if [ "$IN_DOCKER" = true ]; then
    # Directamente ejecutamos el módulo de python
    python -m app.db.seed
else
    # Usamos docker compose desde fuera
    if docker compose version > /dev/null 2>&1; then
        docker compose exec -T backend python -m app.db.seed
    else
        docker-compose exec -T backend python -m app.db.seed
    fi
fi

success "✅ ¡Base de datos poblada con éxito!"