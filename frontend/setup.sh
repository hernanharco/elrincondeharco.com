#!/bin/bash
# Portfolio elRincondeHarco - Frontend Management Script
set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log()     { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Configuración
IMAGE_NAME="portfolio-frontend"
CONTAINER_NAME="portfolio-frontend-app"
PORT=4321

# 1. Cargar PUBLIC_API_URL desde .env
if [ -f .env ]; then
    log "📄 Cargando variables desde frontend/.env..."
    # Extraer solo PUBLIC_API_URL para pasarla como build-arg
    API_URL=$(grep PUBLIC_API_URL .env | cut -d '=' -f2)
else
    API_URL="http://localhost:8000"
    log "⚠️  No se encontró .env, usando por defecto: $API_URL"
fi

case "${1:-help}" in
    "build")
        log "Construyendo imagen de Astro (puedo tardar un poco)..."
        docker build --build-arg PUBLIC_API_URL="$API_URL" -t $IMAGE_NAME .
        success "Imagen $IMAGE_NAME construida."
        ;;
    "up")
        log "Levantando contenedor en puerto $PORT..."
        # Detener si ya existe
        docker rm -f $CONTAINER_NAME 2>/dev/null || true
        docker run -d --name $CONTAINER_NAME -p $PORT:4321 $IMAGE_NAME
        success "Frontend disponible en http://localhost:$PORT"
        ;;
    "stop")
        log "Deteniendo contenedor..."
        docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME
        success "Contenedor eliminado."
        ;;
    "logs")
        docker logs -f $CONTAINER_NAME
        ;;
    *)
        echo "Uso: $0 {build|up|stop|logs}"
        exit 1
        ;;
esac