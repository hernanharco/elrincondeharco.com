#!/bin/bash

# Portfolio elRincondeHarco - Docker Setup Script
# Este script configura y ejecuta los contenedores Docker para desarrollo y producción

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Funciones de utilidad
log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

check_dependencies() {
    log "Verificando dependencias..."
    
    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado. Por favor instálalo primero."
        exit 1
    fi
    
    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose no está instalado. Por favor instálalo primero."
        exit 1
    fi
    
    # Verificar archivos .env en cada carpeta
    if [ ! -f frontend/.env ]; then
        warning "Archivo frontend/.env no encontrado. Creando uno con valores por defecto..."
        cat > frontend/.env << 'ENVEOF'
# Frontend Environment Variables
NODE_ENV=production
FRONTEND_URL=http://localhost:4321
PUBLIC_API_URL=http://localhost:8000
ENVEOF
    fi
    
    if [ ! -f backend/.env ]; then
        warning "Archivo backend/.env no encontrado. Creando uno con valores por defecto..."
        cat > backend/.env << 'ENVEOF'
# Backend Environment Variables
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
ENVEOF
    fi

    # Copiar frontend/.env a la raíz para que docker-compose pueda
    # interpoler ${PUBLIC_API_URL} en el build args del frontend
    log "Sincronizando .env raíz desde frontend/.env..."
    cp frontend/.env .env
    success ".env raíz sincronizado correctamente"
}

build_images() {
    log "Construyendo imágenes Docker..."
    docker-compose build
    if [ $? -eq 0 ]; then
        success "Imágenes construidas correctamente"
    else
        error "Error al construir las imágenes"
        exit 1
    fi
}

start_dev() {
    log "Iniciando entorno de desarrollo..."
    check_dependencies
    
    # Iniciar contenedores en modo desarrollo
    docker-compose up --build
}

start_prod() {
    log "Iniciando entorno de producción..."
    check_dependencies
    
    # Iniciar contenedores en modo producción
    docker-compose -f docker-compose.yml up --build -d
}

stop_services() {
    log "Deteniendo servicios..."
    docker-compose down
}

clean() {
    log "Limpiando recursos..."
    docker-compose down --volumes --remove-orphans
    docker system prune -f
}

logs() {
    log "Mostrando logs de servicios..."
    docker-compose logs -f
}

status() {
    log "Estado de los servicios:"
    docker-compose ps
}

show_help() {
    echo "Portfolio elRincondeHarco - Docker Setup"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos disponibles:"
    echo "  build     - Construir imágenes Docker"
    echo "  dev       - Iniciar entorno de desarrollo"
    echo "  prod      - Iniciar entorno de producción"
    echo "  stop      - Detener todos los servicios"
    echo "  clean     - Limpiar contenedores y volúmenes"
    echo "  logs      - Mostrar logs de los servicios"
    echo "  status    - Ver estado de los servicios"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 dev       # Iniciar en modo desarrollo"
    echo "  $0 prod      # Iniciar en modo producción"
    echo "  $0 logs      # Ver logs del backend"
    echo ""
    echo "Variables de entorno requeridas (.env por carpeta):"
    echo "  frontend/.env:"
    echo "    - NODE_ENV"
    echo "    - FRONTEND_URL"
    echo "    - PUBLIC_API_URL"
    echo "  backend/.env:"
    echo "    - DATABASE_URL"
    echo "    - SECRET_KEY"
    echo "    - CLOUDINARY_CLOUD_NAME"
    echo "    - CLOUDINARY_API_KEY"
    echo "    - CLOUDINARY_API_SECRET"
    echo "    - FRONTEND_URL"
}

# Menú principal
case "${1:-help}" in
    "build")
        build_images
        ;;
    "dev")
        start_dev
        ;;
    "prod")
        start_prod
        ;;
    "stop")
        stop_services
        ;;
    "clean")
        clean
        ;;
    "logs")
        logs
        ;;
    "status")
        status
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        error "Comando no reconocido: $1"
        echo "Usa '$0 help' para ver los comandos disponibles."
        exit 1
        ;;
esac