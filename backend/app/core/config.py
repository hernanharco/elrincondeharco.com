import json
from typing import Any, List
from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configuración agnóstica para elRincondeHarco."""

    # Base de Datos (Obligatorias en el entorno)
    pg_host: str = Field(..., alias="PGHOST")
    pg_port: int = Field(5432, alias="PGPORT")
    pg_database: str = Field(..., alias="PGDATABASE")
    pg_user: str = Field(..., alias="PGUSER")
    pg_password: str = Field(..., alias="PGPASSWORD")
    pg_schema: str = Field(..., alias="PGSCHEMA")
    pg_sslmode: str = Field("disable", alias="PGSSLMODE")

    # Seguridad y Aplicación
    debug: bool = Field(False, alias="DEBUG")
    secret_key: str = Field(..., alias="SECRET_KEY")

    # Cloudinary
    cloudinary_cloud_name: str = Field(..., alias="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(..., alias="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(..., alias="CLOUDINARY_API_SECRET")

    # authCore — validación de JWT
    authcore_jwks_url: str = Field(
        "http://localhost:8000/.well-known/jwks.json",
        alias="AUTHCORE_JWKS_URL",
    )

    @computed_field
    @property
    def database_url(self) -> str:
        """Construye la URL de conexión con aislamiento de Schema."""
        # El parámetro 'options' asegura que el proyecto viva en su propio mundo
        return (
            f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@"
            f"{self.pg_host}:{self.pg_port}/{self.pg_database}?"
            f"options=-csearch_path%3D{self.pg_schema}&"
            f"sslmode={self.pg_sslmode}"
        )

    # CORS Configuration
    cors_origins: List[str] = Field(default_factory=list, alias="CORS_ORIGINS")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, list): return v
        if isinstance(v, str):
            if v.startswith("["): return json.loads(v)
            return [i.strip() for i in v.split(",")]
        return []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

# Instancia global
settings = Settings()