"""
Exceptions — Manejo global de errores para Portfolio API.

Formato de respuesta consistente para TODOS los errores:
{
    "detail": "Mensaje descriptivo",
    "code": "ERROR_CODE",
    "status_code": 404
}
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
import logging
import traceback

logger = logging.getLogger(__name__)


# ── Códigos de error estándar ────────────────────────────────
ERROR_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    413: "PAYLOAD_TOO_LARGE",
    422: "VALIDATION_ERROR",
    429: "TOO_MANY_REQUESTS",
    500: "INTERNAL_ERROR",
    502: "BAD_GATEWAY",
    503: "SERVICE_UNAVAILABLE",
}


def _error_response(status_code: int, detail: str) -> JSONResponse:
    """Construye una respuesta de error con formato consistente."""
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": detail,
            "code": ERROR_CODES.get(status_code, "UNKNOWN_ERROR"),
            "status_code": status_code,
        },
    )


# ── Handlers globales ─────────────────────────────────────────

async def global_exception_handler(request: Request, exc: Exception):
    """
    Handler para excepciones NO controladas (500).
    Loggea el traceback completo y devuelve error genérico.
    """
    logger.error(
        "❌ Error no controlado en %s %s:\n%s",
        request.method,
        request.url.path,
        traceback.format_exc(),
    )
    return _error_response(500, "Error interno del servidor")


async def http_exception_global_handler(request: Request, exc: HTTPException):
    """
    Handler para HTTPException (FastAPI nativas).
    Les da formato consistente.
    """
    return _error_response(exc.status_code, exc.detail)
