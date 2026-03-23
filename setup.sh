#!/bin/bash

# Portfolio elRincondeHarco - Docker Setup Script
set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log()     { echo -e "${BLUE}[INFO]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }

check_dependencies() {
    log "Verificando dependencias..."

    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado. Por favor instálalo primero."
    fi

    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose no está instalado. Por favor instálalo primero."
    fi

    # Verificar y crear frontend/.env si no existe
    if [ ! -f frontend/.env ]; then
        warning "Archivo frontend/.env no encontrado. Creando uno con valores por defecto..."
        cat > frontend/.env << 'ENVEOF'
NODE_ENV=production
FRONTEND_URL=http://localhost:4321
PUBLIC_API_URL=http://localhost:8000
ENVEOF
    fi

    # Sincronizar .env raíz desde frontend/.env para que docker-compose
    # pueda interpolar ${PUBLIC_API_URL} en el build args
    log "Sincronizando .env raíz desde frontend/.env..."
    cp frontend/.env .env
    success ".env raíz sincronizado"
}

set_backend_env() {
    local mode=$1

    if [ "$mode" = "local" ]; then
        if [ ! -f backend/.env.local ]; then
            error "Falta backend/.env.local — copia backend.env.local y rellena los valores."
        fi
        log "Usando base de datos LOCAL (Docker Postgres)..."
        cp backend/.env.local backend/.env
        success "backend/.env → local"

    elif [ "$mode" = "prod" ]; then
        if [ ! -f backend/.env.production ]; then
            error "Falta backend/.env.production — copia backend.env.production y rellena los valores."
        fi
        log "Usando base de datos NEON (producción)..."
        cp backend/.env.production backend/.env
        success "backend/.env → producción (Neon)"
    fi
}

show_db_info() {
    echo ""
    echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║         CONEXIÓN A LA BASE DE DATOS LOCAL (DBeaver)          ║${NC}"
    echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BOLD}  Abre DBeaver → Nueva Conexión → PostgreSQL${NC}"
    echo ""
    echo -e "${YELLOW}  ┌─────────────────────────────────────────┐${NC}"
    echo -e "${YELLOW}  │  Host:      ${NC}${BOLD}localhost${NC}"
    echo -e "${YELLOW}  │  Port:      ${NC}${BOLD}5432${NC}"
    echo -e "${YELLOW}  │  Database:  ${NC}${BOLD}neondb${NC}"
    echo -e "${YELLOW}  │  Username:  ${NC}${BOLD}neondb_owner${NC}"
    echo -e "${YELLOW}  │  Password:  ${NC}${BOLD}localpassword${NC}"
    echo -e "${YELLOW}  │  SSL:       ${NC}${BOLD}desactivado${NC}"
    echo -e "${YELLOW}  └─────────────────────────────────────────┘${NC}"
    echo ""
    echo -e "${BOLD}  URL de conexión directa:${NC}"
    echo -e "  ${CYAN}postgresql://neondb_owner:localpassword@localhost:5432/neondb${NC}"
    echo ""
    echo -e "${BOLD}  Pasos en DBeaver:${NC}"
    echo -e "  1. Click en ${BOLD}Nueva Conexión${NC} (icono del enchufe con +)"
    echo -e "  2. Selecciona ${BOLD}PostgreSQL${NC}"
    echo -e "  3. Rellena los datos de arriba"
    echo -e "  4. En la pestaña ${BOLD}SSL${NC} → desactiva ${BOLD}Use SSL${NC}"
    echo -e "  5. Click ${BOLD}Test Connection${NC} → debería decir Connected ✓"
    echo -e "  6. Click ${BOLD}Finish${NC}"
    echo ""
    echo -e "${BOLD}  Verificar que el contenedor DB está corriendo:${NC}"
    echo -e "  ${CYAN}docker ps | grep db${NC}"
    echo ""
    echo -e "${BOLD}${CYAN}══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

start_dev() {
    log "Iniciando entorno de desarrollo..."
    check_dependencies
    set_backend_env "local"
    docker-compose up --build
}

start_prod() {
    log "Iniciando entorno de producción..."
    check_dependencies
    set_backend_env "local"
    docker-compose -f docker-compose.yml up --build -d
    show_db_info
}

start_prod_neon() {
    log "Iniciando entorno de producción con Neon..."
    check_dependencies
    set_backend_env "prod"
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

db_info() {
    # Verificar si el contenedor está corriendo antes de mostrar info
    if docker ps | grep -q "postgres\|db"; then
        show_db_info
    else
        warning "El contenedor de base de datos no está corriendo."
        echo -e "  Ejecuta primero: ${CYAN}./setup.sh prod${NC}"
        echo ""
        show_db_info
    fi
}

show_help() {
    echo "Portfolio elRincondeHarco - Docker Setup"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos disponibles:"
    echo "  dev        - Desarrollo con Postgres local (Docker)"
    echo "  prod       - Producción simulada con Postgres local (Docker)"
    echo "  prod-neon  - Producción real con base de datos Neon"
    echo "  db-info    - Mostrar datos de conexión para DBeaver"
    echo "  stop       - Detener todos los servicios"
    echo "  clean      - Limpiar contenedores y volúmenes"
    echo "  logs       - Mostrar logs de los servicios"
    echo "  status     - Ver estado de los servicios"
    echo "  help       - Mostrar esta ayuda"
    echo ""
    echo "Archivos .env requeridos:"
    echo "  frontend/.env"
    echo "  backend/.env.local       ← apunta a Docker Postgres"
    echo "  backend/.env.production  ← apunta a Neon"
}

case "${1:-help}" in
    "dev")        start_dev ;;
    "prod")       start_prod ;;
    "prod-neon")  start_prod_neon ;;
    "db-info")    db_info ;;
    "stop")       stop_services ;;
    "clean")      clean ;;
    "logs")       logs ;;
    "status")     status ;;
    "help"|"-h"|"--help") show_help ;;
    *)
        error "Comando no reconocido: $1"
        echo "Usa '$0 help' para ver los comandos disponibles."
        exit 1
        ;;
esac