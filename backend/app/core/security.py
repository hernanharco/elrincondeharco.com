"""
Security — Dependencias de autenticación y autorización para Portfolio.

Cadena de validación:
  1. Token válido (JWT firmado por authCore)
  2. Tenant correcto (el JWT pertenece a este servicio)
  3. Módulo habilitado (el tenant tiene el módulo activo)
  4. Proveedor habilitado (el tenant tiene el proveedor activo)

Excepción: SUPERADMIN puede acceder a todo sin restricción de tenant.
"""

from typing import Dict, Any, List, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.services.auth.TokenValidator import verify_token

bearer_scheme = HTTPBearer(auto_error=False)

# Tenant slug esperado para este servicio (configurar por proyecto)
# Ejemplo: rincom -> "rincom", nanatamoda -> "nanatamoda"
EXPECTED_TENANT_SLUG = getattr(settings, "tenant_slug", None)


def _extract_token_from_cookie(request: Request) -> Optional[str]:
    """Extrae el JWT de la cookie access_token si existe."""
    token = request.cookies.get("access_token")
    return token if token else None


# ══════════════════════════════════════════════════════════════════
# BASE — Obtener usuario del JWT
# ══════════════════════════════════════════════════════════════════

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    request: Request = None,
) -> Dict[str, Any]:
    """
    Dependencia base: valida el JWT y retorna los claims.
    En DEBUG, retorna un usuario de prueba con tenant y modules.
    """
    if settings.debug:
        return {
            "sub": "dev-user",
            "role": "SUPERADMIN",
            "username": "dev",
            "tenant": {"id": "dev-tenant", "slug": "rincom", "name": "Dev Tenant"},
            "modules": {"radar": {"enabled": True}, "inventory": {"enabled": True, "providers": ["vinted", "micolet"]}},
        }

    token = None
    if credentials is not None:
        token = credentials.credentials
    if token is None and request is not None:
        token = _extract_token_from_cookie(request)

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere token de autenticación")

    payload = await verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    return payload


# ══════════════════════════════════════════════════════════════════
# HELPERS — Leer datos del JWT
# ══════════════════════════════════════════════════════════════════

def get_tenant(user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extrae { id, slug, name } del tenant."""
    return user.get("tenant")

def get_tenant_slug(user: Dict[str, Any]) -> Optional[str]:
    """Retorna el slug del tenant."""
    tenant = get_tenant(user)
    return tenant.get("slug") if tenant else None

def get_modules(user: Dict[str, Any]) -> Dict[str, Any]:
    """Extrae los módulos activos."""
    return user.get("modules", {})

def has_module(user: Dict[str, Any], module_id: str) -> bool:
    """Verifica si el usuario tiene un módulo habilitado."""
    modules = get_modules(user)
    module_config = modules.get(module_id)
    return module_config.get("enabled", False) if module_config else False

def get_module_providers(user: Dict[str, Any], module_id: str) -> List[str]:
    """Retorna proveedores habilitados para un módulo."""
    modules = get_modules(user)
    return modules.get(module_id, {}).get("providers", [])

def has_provider(user: Dict[str, Any], module_id: str, provider: str) -> bool:
    """Verifica si un proveedor específico está habilitado."""
    return provider in get_module_providers(user, module_id)

def is_superadmin(user: Dict[str, Any]) -> bool:
    """Verifica si el usuario es SUPERADMIN."""
    return user.get("role", "").upper() == "SUPERADMIN"


# ══════════════════════════════════════════════════════════════════
# GUARDS — Dependencias FastAPI para proteger endpoints
# ══════════════════════════════════════════════════════════════════

async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """Verifica que el usuario esté activo."""
    return current_user


async def get_current_admin_user(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """Solo admins y superadmins. SUPERADMIN bypass total."""
    if settings.debug or is_superadmin(current_user):
        return current_user
    role = current_user.get("role", "").upper()
    if role not in ("SUPERADMIN", "ADMIN"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requieren permisos de administrador")
    return current_user


def require_tenant(expected_slug: str = None):
    """
    Factory que valida que el JWT pertenece a este servicio.

    SUPERADMIN bypass: puede acceder a cualquier tenant.

    Uso:
        @router.get("/admin")
        def admin_page(user = Depends(require_tenant("rincom"))):
            # Solo usuarios de rincom (o SUPERADMIN) llegan aquí
            ...
    """
    slug = expected_slug or EXPECTED_TENANT_SLUG

    async def _guard(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        # SUPERADMIN bypass
        if is_superadmin(user):
            return user

        user_slug = get_tenant_slug(user)
        if not user_slug:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario sin tenant asignado")

        if slug and user_slug != slug:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: tu tenant es '{user_slug}', no '{slug}'",
            )
        return user
    return _guard


def require_module(module_id: str, provider: str = None):
    """
    Factory que valida acceso a un módulo.

    SUPERADMIN bypass: puede acceder a cualquier módulo.

    Uso:
        @router.get("/inventory/vinted")
        def sync_vinted(user = Depends(require_module("inventory", "vinted"))):
            ...
    """
    async def _guard(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        # SUPERADMIN bypass
        if is_superadmin(user):
            return user

        if not has_module(user, module_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Módulo '{module_id}' no habilitado")

        if provider and not has_provider(user, module_id, provider):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Proveedor '{provider}' no habilitado")

        return user
    return _guard
