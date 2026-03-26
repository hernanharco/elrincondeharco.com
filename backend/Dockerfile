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

# --- MEJORA DE AUTOCURACIÓN ---
# 1. Instalamos poetry
# 2. Desactivamos venv (usamos el global de la imagen)
# 3. Sincronizamos el lock al vuelo para evitar el error de "changed significantly"
# 4. Instalamos solo lo necesario para producción
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry lock --no-update && \
    poetry install --only main --no-root
# ------------------------------

# Copy application code
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY alembic.ini ./alembic.ini

# --- CONFIGURACIÓN DEL ENTRYPOINT ---
COPY scripts/entrypoint.sh ./scripts/entrypoint.sh
RUN chmod +x ./scripts/entrypoint.sh
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

# USAR EL ENTRYPOINT PARA PREPARAR LA DB
ENTRYPOINT ["./scripts/entrypoint.sh"]

# Start the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]