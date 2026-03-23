#!/bin/bash

# Portfolio elRincondeHarco - Seed Database Only
# Ejecuta backend/app/db/seed.py cargando configuración desde .env
set -e

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log()     { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# =============================================================================
# ⚙️ CARGAR VARIABLES DE ENTORNO DESDE .env
# =============================================================================
load_env() {
    local env_file=""
    
    # Buscar el archivo .env en orden de prioridad
    if [ -f "backend/.env" ]; then
        env_file="backend/.env"
    elif [ -f "backend/.env.local" ]; then
        env_file="backend/.env.local"
    elif [ -f ".env" ]; then
        env_file=".env"
    else
        warning "⚠️  No se encontró archivo .env, usando valores por defecto..."
        export PGHOST="db"
        export PGDATABASE="neondb"
        export PGUSER="neondb_owner"
        export PGPASSWORD="localpassword"
        return 0
    fi
    
    log "📄 Cargando variables desde: $env_file"
    
    # Exportar variables del .env (ignorando comentarios y líneas vacías)
    set -a
    source <(grep -E '^[A-Z_]+=.+$' "$env_file" | sed 's/#.*//')
    set +a
    
    success "✅ Variables de entorno cargadas"
}

# =============================================================================
# ⚙️ CONFIGURACIÓN (ahora desde .env)
# =============================================================================
# DB_SERVICE: nombre del servicio en docker-compose.yml (NO es el nombre de la BD)
# Por defecto usa PGHOST, que debería ser "db" según tu configuración
DB_SERVICE="${PGHOST:-db}"
DB_USER="${PGUSER:-neondb_owner}"
DB_NAME="${PGDATABASE:-neondb}"
MAX_RETRIES=30

# =============================================================================
# 🗄️  ESPERAR POSTGRES
# =============================================================================
wait_for_db() {
    log "⏳ Esperando a que PostgreSQL esté listo en servicio: $DB_SERVICE..."
    for i in $(seq 1 $MAX_RETRIES); do
        if docker-compose exec -T "$DB_SERVICE" pg_isready -U "$DB_USER" -d "$DB_NAME" &>/dev/null; then
            success "✅ PostgreSQL listo"
            return 0
        fi
        echo -n "."
        sleep 2
    done
    echo ""
    error "❌ PostgreSQL no respondió después de $((MAX_RETRIES * 2)) segundos"
}

# =============================================================================
# 🌱 EJECUTAR SEED
# =============================================================================
run_seed() {
    log "🚀 Ejecutando backend/app/db/seed.py..."
    
    # Ejecutar el script de seed dentro del contenedor backend
    # El contenedor backend ya tiene sus propias variables de entorno
    docker-compose exec -T backend python -m app.db.seed
    
    if [ $? -eq 0 ]; then
        success "✅ Seed completado exitosamente"
    else
        error "❌ El seed falló. Revisa los logs con: ./setup.sh logs"
    fi
}

# =============================================================================
# 🎯 MAIN
# =============================================================================
main() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  🌱 Seed de Base de Datos - elRincondelHarco  ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    
    # 1. Cargar variables de entorno desde .env
    load_env
    
    # 2. Verificar que docker-compose esté disponible
    if ! command -v docker-compose &>/dev/null; then
        error "Docker Compose no está instalado"
    fi
    
    # 3. Verificar que los contenedores estén corriendo
    if ! docker-compose ps | grep -q "Up"; then
        warning "⚠️  No hay contenedores activos."
        echo -e "  Ejecuta primero: ${BLUE}./setup.sh prod${NC}"
        echo ""
        read -p "¿Quieres intentar ejecutar el seed de todas formas? (s/N): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Ss]$ ]]; then
            exit 0
        fi
    fi
    
    # 4. Esperar BD y ejecutar seed
    wait_for_db
    run_seed
    
    echo ""
    success "🎉 ¡Todo listo! Tu portfolio tiene datos iniciales."
    echo -e "  Accede en: ${BLUE}http://localhost:4321${NC}"
    echo ""
}

# Ejecutar
main "$@"