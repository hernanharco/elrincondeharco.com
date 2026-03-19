from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings v2."""

    # Mapeo directo desde el archivo .env
    pg_host: str = Field(..., alias="PGHOST")
    pg_database: str = Field(..., alias="PGDATABASE")
    pg_user: str = Field(..., alias="PGUSER")
    pg_password: str = Field(..., alias="PGPASSWORD")
    pg_sslmode: str = Field("require", alias="PGSSLMODE")
    pg_channel_binding: str = Field("require", alias="PGCHANNELBINDING")

    # Application
    debug: bool = True
    secret_key: str = "your-secret-key-change-in-production"

    # Cloudinary
    cloudinary_cloud_name: str = Field(..., env="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str = Field(..., env="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str = Field(..., env="CLOUDINARY_API_SECRET")

    @computed_field
    @property
    def database_url(self) -> str:
        """
        Construye la URL de conexión para Neon PostgreSQL (Psycopg 3).
        Siguiendo el principio de 'Menos infraestructura, más valor'.
        """
        return (
            f"postgresql+psycopg://{self.pg_user}:{self.pg_password}@"
            f"{self.pg_host}/{self.pg_database}?"
            f"sslmode={self.pg_sslmode}&"
            f"channel_binding={self.pg_channel_binding}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignora otras variables del .env que no necesitemos aquí
    )


# Instancia única para toda la app
settings = Settings()
