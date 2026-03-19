from contextlib import asynccontextmanager
from datetime import datetime
from zoneinfo import ZoneInfo
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine
from app.models.base import Base
from app.api.route import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting FastAPI app in development mode")
    local_tz = ZoneInfo("Europe/Madrid")
    local_time = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")
    print(f"🌍 Timezone: {local_tz} | 🕒 Local Time: {local_time}")

    print("--- Verificando conexión a NEON (development) ---")
    try:
        async with engine.begin() as conn:
            # Función interna para inspeccionar tablas existentes
            def get_tables(connection):
                from sqlalchemy import inspect

                return inspect(connection).get_table_names()

            existing_tables = await conn.run_sync(get_tables)
            metadata_tables = Base.metadata.tables.keys()

            # Solo ejecutamos si hay modelos en código que no están en la DB
            new_tables = [t for t in metadata_tables if t not in existing_tables]

            await conn.run_sync(Base.metadata.create_all)

            if new_tables:
                print(f"✅ Nuevas tablas creadas/detectadas: {', '.join(new_tables)}")
            else:
                print("info: Schema sincronizado (sin cambios pendientes)")

    except Exception as e:
        print(f"❌ Error en DB: {str(e)}", file=sys.stderr)
        raise
    yield
    await engine.dispose()


app = FastAPI(
    title="Auth Core Backend",
    description="Backend de autenticación con FastAPI y Neon Postgres",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc (opcional)
    openapi_url="/openapi.json",
)


app.include_router(api_router, prefix="/api/v1")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "✅ Backend está corriendo correctamente"}


@app.get("/health")
async def health_check():
    # Puedes mejorar esto más adelante verificando realmente la conexión
    return {"status": "healthy", "database": "connected (verificado en startup)"}
