"""
WhatsApp Cloud API Webhook — Recibe mensajes entrantes desde Meta.

Meta llama a este endpoint cuando alguien escribe al número de WhatsApp.
Se encarga de validar el webhook (GET) y procesar mensajes (POST).
"""

import logging
import os
from typing import Optional

from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse

logger = logging.getLogger(__name__)

router = APIRouter()

# Token de verificación configurable via entorno
VERIFY_TOKEN = "***REMOVED***"

# URL del Radar backend para reenviar mensajes
# En Docker: radar-harco-api:3005 (misma red)
# En local: localhost:3005
RADAR_API_URL = os.getenv("RADAR_API_URL", "http://localhost:3005")


@router.get("/webhook")
async def verify_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
):
    """
    Meta verifica el webhook con una petición GET.
    Si el token coincide, respondemos con el challenge.
    """
    logger.info(f"Webhook verification: mode={hub_mode}, token={hub_verify_token}")

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        logger.info("Webhook verificado correctamente")
        return PlainTextResponse(hub_challenge)

    logger.warning("Webhook verification failed")
    return PlainTextResponse("Verification failed", status_code=403)


@router.post("/webhook")
async def receive_webhook(request: Request):
    """
    Recibe mensajes entrantes desde Meta.
    Los reenvía al Radar backend para procesamiento.
    """
    try:
        body = await request.json()
        logger.info(f"Webhook received: {body}")

        # Extraer mensajes del payload de Meta
        entry = body.get("entry", [])
        for e in entry:
            changes = e.get("changes", [])
            for change in changes:
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    # Reenviar al Radar backend
                    import httpx

                    async with httpx.AsyncClient() as client:
                        await client.post(
                            f"{RADAR_API_URL}/api/whatsapp/webhook",
                            json={
                                "from": msg.get("from"),
                                "text": msg.get("text", {}).get("body", ""),
                                "timestamp": msg.get("timestamp"),
                                "msg_id": msg.get("id"),
                                "source": "cloud_api",
                                "instance": "harco",
                            },
                            timeout=5.0,
                        )

        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
