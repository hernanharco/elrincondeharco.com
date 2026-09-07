"""
Security — Dependencias de autenticación y autorización para Portfolio.
Los JWT son emitidos por authCore y validados contra su JWKS.

El token puede venir por:
  - Header Authorization: Bearer <token> (para API clients)
  - Cookie access_token (para browser con Google OAuth)

El JWT enriquecido incluye:
  - sub, username, email, role (datos del usuario)
  - tenant: { id, slug, name } (empresa a la que pertenece)
  - modules: { radar: { enabled }, inventory: { enabled, providers: [...] } } (feature flags)
"""

from typing import Dict, Any, List, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.services.auth.TokenValidator import verify_token

# Esquema de seguridad: espera el token en header Authorization: Bearer <token>
bearer_scheme = HTTPBearer(auto_error=False)


def _extract_token_from_cookie(request: Request) -> Optional[str]:
    """Extrae el JWT de la cookie access_token si existe."""
    token = request.cookies.get("access_token")
    return token if token else None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    request: Request = None,
) -> Dict[str, Any]:
    """
    Dependencia base: valida el JWT y retorna los claims del usuario.

    Orden de búsqueda del token:
    1. Header Authorization: Bearer <token>
    2. Cookie access_token (para Google OAuth desde browser)

    En modo DEBUG (desarrollo) se salta la validación.

    Returns:
        Dict con: sub, username, email, role, tenant, modules, etc.

    Raises:
        401 si el token falta o es inválido.
    """
    # En desarrollo, bypasseamos auth para facilitar el desarrollo del CRM
    if settings.debug:
        return {
            "sub": "dev-user",
            "role": "ADMIN",
            "username": "dev",
            "tenant": {"id": "dev-tenant", "slug": "rincom", "name": "Dev Tenant"},
            "modules": {"radar": {"enabled": True}, "inventory": {"enabled": True, "providers": ["vinted", "micolet"]}},
        }

    token = None

    # 1. Intentar desde header Bearer
    if credentials is not None:
        token = credentials.credentials

    # 2. Si no hay header, intentar desde cookie
    if token is None and request is not None:
        token = _extract_token_from_cookie(request)

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere token de autenticación",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = await verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


# ══════════════════════════════════════════════════════════════════
# HELPERS — Para leer tenant y modules del JWT
# ══════════════════════════════════════════════════════════════════

def get_tenant(user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Extrae la info del tenant del payload del JWT.
    Returns: { id, slug, name } o None si el usuario no tiene tenant.
    """
    return user.get("tenant")


def get_tenant_slug(user: Dict[str, Any]) -> Optional[str]:
    """Retorna el slug del tenant (ej: 'rincom', 'nanatamoda')."""
    tenant = get_tenant(user)
    return tenant.get("slug") if tenant else None


def get_modules(user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extrae los módulos activos del payload del JWT.
    Returns: { "radar": { "enabled": true }, "inventory": { ... } }
    """
    return user.get("modules", {})


def has_module(user: Dict[str, Any], module_id: str) -> bool:
    """
    Verifica si el usuario tiene un módulo habilitado.
    Ej: has_module(user, "radar") → True/False
    """
    modules = get_modules(user)
    module_config = modules.get(module_id)
    if not module_config:
        return False
    return module_config.get("enabled", False)


def get_module_providers(user: Dict[str, Any], module_id: str) -> List[str]:
    """
    Retorna los proveedores habilitados para un módulo.
    Ej: get_module_providers(user, "inventory") → ["vinted", "micolet"]
    """
    modules = get_modules(user)
    module_config = modules.get(module_id, {})
    return module_config.get("providers", [])


def has_provider(user: Dict[str, Any], module_id: str, provider: str) -> bool:
    """
    Verifica si el usuario tiene un proveedor específico habilitado.
    Ej: has_provider(user, "inventory", "vinted") → True/False
    """
    providers = get_module_providers(user, module_id)
    return provider in providers


# ══════════════════════════════════════════════════════════════════
# GUARDS — Dependencias FastAPI para proteger endpoints
# ══════════════════════════════════════════════════════════════════

def require_module(module_id: str, provider: str = None):
    """
    Factory de dependencias que valida acceso a un módulo.

    Uso en endpoints:
        @router.get("/inventory/vinted")
        def sync_vinted(user = Depends(require_module("inventory", "vinted"))):
            # Solo llega si el JWT tiene inventory.enabled + vinted en providers
            ...

        @router.get("/radar")
        def radar_dashboard(user = Depends(require_module("radar"))):
            # Solo llega si el JWT tiene radar.enabled
            ...
    """
    async def _guard(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        if not has_module(user, module_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Módulo '{module_id}' no habilitado para tu empresa",
            )
        if provider and not has_provider(user, module_id, provider):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Proveedor '{provider}' no habilitado en módulo '{module_id}'",
            )
        return user
    return _guard


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Verifica que el usuario esté activo (no bloqueado).
    """
    return current_user


async def get_current_admin_user(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """
    Solo admins y superadmins pueden ejecutar la operación.
    En modo DEBUG (desarrollo) se salta la validación.
    """
    if settings.debug:
        return {"sub": "dev-user", "role": "ADMIN", "username": "dev"}
    role = current_user.get("role", "").upper()
    if role not in ("SUPERADMIN", "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )
    return current_user


async def get_current_admin_user(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """
    Solo admins y superadmins pueden ejecutar la operación.
    En modo DEBUG (desarrollo) se salta la validación.
    """
    if settings.debug:
        return {"sub": "dev-user", "role": "ADMIN", "username": "dev"}
    role = current_user.get("role", "").upper()
    if role not in ("SUPERADMIN", "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )
    return current_user
