import sys
from contextlib import asynccontextmanager
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.core.exceptions import global_exception_handler, http_exception_global_handler
from app.db.session import engine
from app.models.base import Base
from app.api.route import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando Backend...")
    local_tz = ZoneInfo("Europe/Madrid")
    local_time = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Obtener el nombre del esquema desde el .env
    schema_name = settings.pg_schema
    print(f"🌍 {local_time} | Esquema objetivo: {schema_name}")

    try:
        # FASE 1: Crear el esquema físicamente en Postgres si no existe
        async with engine.begin() as conn:
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
            print(f"✨ Infraestructura: Esquema '{schema_name}' asegurado.")

        # FASE 2: Sincronizar modelos FORZANDO el esquema
        async with engine.begin() as conn:
            def sync_models(sync_conn):
                # IMPORTANTE: Forzamos a la Metadata de SQLAlchemy a usar nuestro esquema
                # Esto evita que se "escape" nada a 'public'
                Base.metadata.schema = schema_name
                
                # Opcional: Reforzar en cada tabla individual por si acaso
                for table in Base.metadata.tables.values():
                    table.schema = schema_name
                
                # Crear tablas
                Base.metadata.create_all(bind=sync_conn)

            await conn.run_sync(sync_models)
            print(f"✅ Tablas creadas/verificadas en el esquema: '{schema_name}'")

    except Exception as e:
        print(f"❌ ERROR EN DB: {str(e)}", file=sys.stderr)
        raise e
        
    yield
    await engine.dispose()
    print("🛑 Shutdown completado")

app = FastAPI(
    title="Portfolio API",
    lifespan=lifespan,
)

# ── Exception Handlers Globales ──────────────────────────────
# Formato consistente para TODOS los errores:
# { "detail": "...", "code": "ERROR_CODE", "status_code": 400 }
app.add_exception_handler(HTTPException, http_exception_global_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Cache-Control para endpoints públicos ─────────────────────
# Los GET a /api/v1/ se cachean 60s en el navegador/CDN.
# Los POST/PUT/DELETE no se cachean.
@app.middleware("http")
async def add_cache_control(request: Request, call_next):
    response = await call_next(request)
    if (
        request.method == "GET"
        and response.status_code == 200
        and request.url.path.startswith("/api/v1/")
    ):
        response.headers["Cache-Control"] = "public, max-age=60"
    return response

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "✅ Backend en línea", "schema": settings.pg_schema}