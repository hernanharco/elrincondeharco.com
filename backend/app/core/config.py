import json
from typing import Any, Optional, Union
from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings v2."""

    # Mapeo directo desde el archivo .env (Neon PostgreSQL)
    pg_host: str = Field(..., alias="PGHOST")
    pg_database: str = Field(..., alias="PGDATABASE")
    pg_user: str = Field(..., alias="PGUSER")
    pg_password: str = Field(..., alias="PGPASSWORD")
    pg_sslmode: str = Field("require", alias="PGSSLMODE")
    pg_channel_binding: str = Field("require", alias="PGCHANNELBINDING")

    # Application
    debug: bool = True
    secret_key: str = "your-secret-key-change-in-production"

    # Cloudinary (Simplificado para usar alias del .env igual que PG)
    cloudinary_cloud_name: str = Field(..., alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(..., alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(..., alias="CLOUDINARY_API_SECRET")

    @computed_field
    @property
    def database_url(self) -> str:
        """Construye la URL de conexión para Neon PostgreSQL."""
        return (
            f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@"
            f"{self.pg_host}/{self.pg_database}?"
            f"sslmode={self.pg_sslmode}&"
            f"channel_binding={self.pg_channel_binding}"
        )

    # CORS Configuration
    cors_origins: list[str] = []

    @field_validator("cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, list):
            return v
        if isinstance(v, str) and v.startswith("["):
            return json.loads(v)
        if isinstance(v, str):
            # Esto permite: https://web.com, http://localhost
            return [i.strip() for i in v.split(",")]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

# Instancia única para toda la app
settings = Settings()