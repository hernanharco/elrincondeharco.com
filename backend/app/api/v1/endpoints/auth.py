"""
auth.py — Endpoints de autenticación de Portfolio contra authCore.
El login es proxy inverso hacia authCore; la cookie httpOnly la setea Portfolio.
"""

import logging
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel

from app.core.config import settings
from app.core.security import get_current_active_user
from app.services.auth.TokenValidator import verify_token
import httpx

router = APIRouter()

# ── Schemas ───────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    status: str
    is_active: bool

class LoginResponse(BaseModel):
    user: UserResponse


# ── Endpoints ─────────────────────────────────────────────────

@router.post("/login")
async def login(
    credentials: LoginRequest,
    response: Response,
):
    """
    Proxy inverso a authCore: valida credenciales y setea cookie httpOnly.
    El frontend NUNCA ve el JWT — solo confía en la cookie.
    """
    authcore_url = f"{settings.authcore_jwks_url.removesuffix('/.well-known/jwks.json')}/api/v1/auth/login"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            auth_resp = await client.post(
                authcore_url,
                json={"username": credentials.username, "password": credentials.password},
            )

            if auth_resp.status_code != 200:
                detail = auth_resp.json().get("detail", "Credenciales inválidas")
                raise HTTPException(
                    status_code=auth_resp.status_code,
                    detail=detail,
                )

            auth_data = auth_resp.json()

        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No se pudo contactar con el servidor de autenticación (authCore)",
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="El servidor de autenticación tardó demasiado en responder",
            )

    # Validar el token contra authCore (JWKS) antes de setear la cookie
    token = auth_data["access_token"]
    payload = await verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido recibido de authCore",
        )

    # Setear cookie httpOnly
    expires_in = auth_data.get("expires_in", 3600)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=expires_in,
        path="/",
        samesite="lax",
        secure=not settings.debug,
    )

    logging.info(f"✅ Login exitoso via Portfolio proxy: {credentials.username}")

    return {
        "user": auth_data.get("user", {}),
    }


class SetSessionRequest(BaseModel):
    token: str


@router.post("/set-session")
async def set_session(
    body: SetSessionRequest,
    response: Response,
):
    """
    Recibe un JWT (válido de authCore), lo valida y setea cookie httpOnly.
    Usado por el callback de Google OAuth cuando authCore nos redirige con el token.
    """
    # Validar el token contra authCore (JWKS)
    payload = await verify_token(body.token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )

    # Setear cookie httpOnly
    # El token tiene exp en el payload, pero usamos 24h como max_age para la cookie
    # (el backend valida la exp real del JWT en cada request)
    response.set_cookie(
        key="access_token",
        value=body.token,
        httponly=True,
        max_age=86400,  # 24h
        path="/",
        samesite="lax",
        secure=not settings.debug,
    )

    return {
        "user": {
            "id": payload.get("sub") or payload.get("id", 0),
            "username": payload.get("username", ""),
            "email": payload.get("email", ""),
            "full_name": payload.get("full_name", ""),
            "role": payload.get("role", ""),
            "status": payload.get("status", "active"),
            "is_active": True,
        }
    }


@router.post("/logout")
async def logout(response: Response):
    """
    Limpia la cookie de sesión.
    """
    response.delete_cookie(
        key="access_token",
        path="/",
    )
    return {"message": "Sesión cerrada correctamente"}


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """
    Retorna la información del usuario autenticado.
    Lee el token de la cookie o del header Authorization.
    """
    return UserResponse(
        id=current_user.get("sub") or current_user.get("id", 0),
        username=current_user.get("username", ""),
        email=current_user.get("email", ""),
        full_name=current_user.get("full_name", ""),
        role=current_user.get("role", ""),
        status=current_user.get("status", "active"),
        is_active=current_user.get("is_active", True),
    )
