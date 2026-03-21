import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Importa tu Base y modelos
from app.models.base import Base 
# Importante: Importar los modelos asegura que Base.metadata los conozca
from app.models.hero import Hero
from app.models.about import About
from app.models.passions import Passion
from app.models.projects import Project
from app.models.stack import Stack
from app.models.footer import Footer

# Cargar variables de entorno del .env
load_dotenv()

config = context.config

# Configurar logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Asignar el metadata de tus modelos
target_metadata = Base.metadata

def get_url():
    # Prioridad: Variable de entorno DATABASE_URL
    return os.getenv("DATABASE_URL")

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    # Sobrescribimos la configuración del .ini con la URL real del entorno
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()