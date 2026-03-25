# Use Python 3.12 slim as base
FROM python:3.12-slim

# Install system dependencies (incluimos libpq-dev para psycopg)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

# Copy application code
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini ./alembic.ini

# --- CONFIGURACIÓN DEL ENTRYPOINT ---
# 1. Copiamos el script (asegúrate de que esté en la misma carpeta que el Dockerfile)
COPY scripts/entrypoint.sh ./scripts/entrypoint.sh

# 2. Damos permisos de ejecución como root
RUN chmod +x ./scripts/entrypoint.sh

# 3. Limpieza de finales de línea (por si lo editaste en Windows)
RUN sed -i 's/\r$//' ./scripts/entrypoint.sh
# ------------------------------------

# Create non-root user y cambiar dueño de la carpeta /app
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# Cambiamos al usuario app
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8000/docs"]

# USAR EL ENTRYPOINT PARA PREPARAR LA DB (Crear Schema + Migraciones)
ENTRYPOINT ["./scripts/entrypoint.sh"]

# Start the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]