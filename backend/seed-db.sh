#!/bin/bash
# Portfolio elRincondeHarco - Seed Database Only
set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log()     { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Detectar comando
if docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# 1. Cargar variables
if [ -f ".env" ]; then
    log "📄 Cargando variables desde .env local..."
    export $(grep -v '^#' .env | xargs)
else
    error "No se encontró el archivo .env"
fi

DB_SERVICE="db" # Nombre del servicio en docker-compose.yml

log "⏳ Esperando a que la DB esté lista..."
until $DOCKER_COMPOSE exec -T $DB_SERVICE pg_isready -U ${PGUSER:-neondb_owner} > /dev/null 2>&1; do
  echo -n "."
  sleep 2
done

log "🚀 Ejecutando seed..."
# IMPORTANTE: Usamos el nombre del servicio 'backend' definido en tu compose
$DOCKER_COMPOSE exec -T backend python -m app.db.seed

success "✅ ¡Base de datos poblada con éxito!"