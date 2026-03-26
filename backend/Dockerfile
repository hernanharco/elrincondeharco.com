# 1. Usamos una imagen base ligera de Python 3.12
FROM python:3.12-slim

# 2. Variables de entorno para optimizar Python en Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/tmp/poetry_cache'

# 3. Instalamos dependencias del sistema necesarias (libpq-dev para PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Establecemos el directorio de trabajo
WORKDIR /app

# 5. Copiamos los archivos de dependencias primero (mejor aprovechamiento de caché)
COPY pyproject.toml poetry.lock* ./

# 6. Instalamos Poetry, sincronizamos el lock si hubo cambios y bajamos dependencias
# El comando 'poetry lock --no-update' es el que evita el error que tenías
RUN pip install --no-cache-dir poetry==2.0.1 && \
    poetry lock --no-update && \
    poetry install --only main --no-root && \
    rm -rf $POETRY_CACHE_DIR

# 7. Copiamos el resto del código del proyecto
COPY . .

# 8. Instalamos el proyecto (si fuera necesario para el path)
RUN poetry install --only main

# 9. Exponemos el puerto del backend (FastAPI suele usar 8000 o 8080)
EXPOSE 8000

# 10. Comando para ejecutar la aplicación con Uvicorn
# Ajusta 'main:app' según el nombre de tu archivo de entrada
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]