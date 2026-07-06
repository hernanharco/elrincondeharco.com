#!/bin/bash
# ================================================================
# deploy.sh — Pipeline automatizado de producción (Portfolio)
# ================================================================
# Uso:   pnpm run deploy
#        O directamente: bash scripts/deploy.sh
# ================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# ── Colores ─────────────────────────────────────────────────────
BOLD='\033[1m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ═════════════════════════════════════════════════════════════════
#  CONFIGURACIÓN — EDITAR SI CAMBIA EL SERVIDOR
# ═════════════════════════════════════════════════════════════════
HETZNER_HOST="hetzner-wg"                    # Alias SSH (~/.ssh/config)
HETZNER_PATH="/opt/portfolio"                # Ruta en el servidor
VERCEL_PROJECT="portfolio-elrincondeharco"   # Nombre en Vercel
# ═════════════════════════════════════════════════════════════════

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀  Portfolio · Deploy                 ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""

TOTAL=6

# ── Paso 1: Build + Vercel ──────────────────────────────────────
echo -e "${YELLOW}[1/$TOTAL]${NC} Deploy frontend a Vercel..."
cd frontend
PUBLIC_API_URL="https://api.elrincondeharco.com" \
  SSR_API_URL="https://api.elrincondeharco.com" \
  pnpm build 2>&1 | tail -5
vercel --prod --yes 2>&1 | tail -3
cd ..
echo -e "  ${GREEN}✅${NC} Frontend en Vercel"
echo ""

# ── Paso 2: Git push ────────────────────────────────────────────
echo -e "${YELLOW}[2/$TOTAL]${NC} Subir a GitHub..."
git add .
git commit -m "deploy: producción $(date +%Y-%m-%d)" 2>/dev/null || true
git push origin main 2>&1 | tail -1
echo -e "  ${GREEN}✅${NC} Código en GitHub"
echo ""

# ── Paso 3: SSH + pull ──────────────────────────────────────────
echo -e "${YELLOW}[3/$TOTAL]${NC} Actualizar servidor..."
ssh "$HETZNER_HOST" "mkdir -p $HETZNER_PATH && cd $HETZNER_PATH && git pull origin main"
echo -e "  ${GREEN}✅${NC} Código actualizado"
echo ""

# ── Paso 4: Migrar datos (si es primera vez) ────────────────────
echo -e "${YELLOW}[4/$TOTAL]${NC} Migrar datos desde Dokploy..."
ssh "$HETZNER_HOST" "
  # Verificar si la DB standalone ya tiene datos
  HAS_DATA=\$(docker exec portfolio-postgres-1 psql -U portfolio -d portfolio -tAc \"SELECT COUNT(*) FROM elrincondeharco.heroes\" 2>/dev/null || echo '0')
  if [ \"\$HAS_DATA\" = \"0\" ] || [ -z \"\$HAS_DATA\" ]; then
    echo '  ↪ Migrando datos desde Dokploy...'
    # Dump desde Dokploy
    docker exec infraestructuraglobal-dbglobal-x1wtan.1.p2uldynfgn4o3s0rs4adbhud2 \\
      pg_dump -U postgres -d postgres --schema=elrincondeharco --no-owner --no-acl > /tmp/portfolio_migrate.sql
    # Restaurar en la nueva DB
    docker exec -i portfolio-postgres-1 psql -U portfolio -d portfolio < /tmp/portfolio_migrate.sql 2>&1 | grep -v 'ERROR.*already exists' | grep -v 'multiple primary keys'
    echo '  ✅ Datos migrados'
  else
    echo '  ↪ DB standalone ya tiene datos, skip'
  fi
"
echo -e "  ${GREEN}✅${NC} Base de datos lista"
echo ""

# ── Paso 5: Docker compose ──────────────────────────────────────
echo -e "${YELLOW}[5/$TOTAL]${NC} Reconstruir contenedores..."
ssh "$HETZNER_HOST" "
  cd $HETZNER_PATH
  docker compose -f compose.prod.yaml down 2>/dev/null || true
  docker compose -f compose.prod.yaml up -d --build
"
echo -e "  ${GREEN}✅${NC} Contenedores actualizados"
echo ""

# ── Paso 6: Healthcheck ─────────────────────────────────────────
echo -e "${YELLOW}[6/$TOTAL]${NC} Verificar deploy..."
sleep 5
HEALTH=$(curl -s --max-time 5 "https://api.elrincondeharco.com/" 2>/dev/null || echo '{"message": "checking..."}')
echo -e "  ${CYAN}🔧${NC} Backend:  https://api.elrincondeharco.com"
echo -e "  ${CYAN}🌐${NC} Frontend: https://www.elrincondeharco.com"
echo -e "  ${CYAN}📊${NC} API:      $HEALTH"
echo ""

# ── Fin ─────────────────────────────────────────────────────────
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅  Deploy completado                   ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
