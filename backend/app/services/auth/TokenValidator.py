"""
TokenValidator — Valida JWT emitidos por authCore.

Flujo:
1. Al primer uso, fetchea el JWKS desde authCore
2. Construye la clave pública RSA desde el JWK
3. Verifica el JWT con esa clave pública
4. Cachea la clave para futuras verificaciones
"""

import logging
import time
from typing import Dict, Any, Optional
from jose import jwk, jwt, JWTError
from app.core.config import settings

logger = logging.getLogger(__name__)

# Cache de la clave pública RSA construida desde JWKS
_rsa_key_cache: Optional[jwk.RSAKey] = None
_rsa_key_cache_time: float = 0.0
_JWKS_CACHE_TTL: int = 3600  # 1 hora


async def _fetch_jwks() -> dict:
    """
    Obtiene el JWKS desde authCore.
    Lanza RuntimeError si no puede conectar (ej: authCore no está corriendo).
    """
    import httpx
    async with httpx.AsyncClient(timeout=5.0) as client:
        logger.info("🔑 Fetching JWKS desde %s", settings.authcore_jwks_url)
        try:
            response = await client.get(settings.authcore_jwks_url)
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            raise RuntimeError(
                f"No se puede conectar a authCore en {settings.authcore_jwks_url}. "
                "Asegurate de que authCore esté corriendo."
            )


def _build_rsa_key_from_jwks(jwks: dict) -> jwk.RSAKey:
    """
    Construye una clave RSA desde el primer JWK en el set.
    """
    if "keys" not in jwks or not jwks["keys"]:
        raise ValueError("JWKS vacío o sin keys")

    jwk_data = jwks["keys"][0]
    return jwk.construct(jwk_data, algorithm="RS256")


async def get_rsa_key() -> jwk.RSAKey:
    """
    Retorna la clave pública RSA (con caché con TTL de 1 hora).
    Si el caché expiró, refetchea el JWKS para soportar rotación de claves.
    """
    global _rsa_key_cache, _rsa_key_cache_time
    now = time.time()
    if _rsa_key_cache is None or (now - _rsa_key_cache_time) > _JWKS_CACHE_TTL:
        jwks = await _fetch_jwks()
        _rsa_key_cache = _build_rsa_key_from_jwks(jwks)
        _rsa_key_cache_time = now
        logger.info("✅ Clave RSA cargada desde authCore JWKS")
    return _rsa_key_cache


async def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifica un JWT firmado por authCore.

    Returns:
        Dict con los claims del token (sub, username, role, etc.)
        o None si el token es inválido/expirado.
    """
    try:
        key = await get_rsa_key()
        payload = jwt.decode(token, key, algorithms=["RS256"])
        return payload
    except JWTError as e:
        logger.warning("Token inválido: %s", e)
        return None


def invalidate_cache():
    """Invalida el caché (útil si authCore rota las claves)."""
    global _rsa_key_cache, _rsa_key_cache_time
    _rsa_key_cache = None
    _rsa_key_cache_time = 0.0
