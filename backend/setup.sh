#!/bin/bash
# Portfolio elRincondeHarco - Backend Setup Script
set -e

# Colores para output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log()     { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Detectar comando docker compose
if docker compose version > /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

check_env() {
    if [ ! -f .env ]; then
        error "Archivo .env no encontrado en la carpeta backend. Por favor, créalo."
    fi
}

case "${1:-help}" in
    "prod")
        log "Iniciando Backend + DB en modo producción..."
        check_env
        $DOCKER_COMPOSE up --build -d
        success "Servicios iniciados en segundo plano."
        ;;
    "stop")
        log "Deteniendo servicios..."
        $DOCKER_COMPOSE down
        ;;
    "logs")
        $DOCKER_COMPOSE logs -f
        ;;
    "status")
        $DOCKER_COMPOSE ps
        ;;
    *)
        echo "Uso: $0 {prod|stop|logs|status}"
        exit 1
        ;;
esac