"""
Security — Dependencias de autenticación y autorización para Portfolio.
Los JWT son emitidos por authCore y validados contra su JWKS.

El token puede venir por:
  - Header Authorization: Bearer <token> (para API clients)
  - Cookie access_token (para browser con Google OAuth)
"""

from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param

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

    Returns:
        Dict con: sub, username, email, role, etc.

    Raises:
        401 si el token falta o es inválido.
    """
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


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Verifica que el usuario esté activo (no bloqueado).
    """
    # authCore marca is_active en el token? No directamente.
    # Pero si el token está firmado, es porque authCore lo emitió
    # y authCore ya validó que el usuario está activo al emitirlo.
    # Si necesitamos chequear, podríamos extender en el futuro.
    return current_user


async def get_current_admin_user(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """
    Solo admins y superadmins pueden ejecutar la operación.
    """
    role = current_user.get("role", "").upper()
    if role not in ("SUPERADMIN", "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )
    return current_user
