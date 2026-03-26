#!/bin/bash
set -e

# 1. Esperar a que la DB esté disponible
echo "🔍 Comprobando conexión con el host '${PGHOST:-global-db}'..."

python -c "
import socket
import time
import os

host = os.getenv('PGHOST', 'global-db')
port = int(os.getenv('PGPORT', 5432))

print(f'⏳ Esperando a que {host}:{port} acepte conexiones...')
start_time = time.time()
while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            print('✅ ¡Conexión establecida!')
            break
    except (socket.timeout, ConnectionRefusedError, socket.gaierror):
        if time.time() - start_time > 30:
            print('❌ ERROR: Tiempo de espera agotado conectando a la DB.')
            exit(1)
        time.sleep(1)
"

# 2. Asegurar el Schema
echo "🛠️ Asegurando que el mundo '${PGSCHEMA}' exista..."
python -c "
from sqlalchemy import create_engine, text
import os
url = os.getenv('DATABASE_URL')
schema = os.getenv('PGSCHEMA')
if not url or not schema:
    print('❌ Error: DATABASE_URL o PGSCHEMA no definidos.')
    exit(1)

engine = create_engine(url)
with engine.connect() as conn:
    conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema}'))
    conn.commit()
    print(f'✅ Schema {schema} verificado.')
"

# 3. Migraciones (Con captura de errores para evitar paros críticos)
echo "📑 Ejecutando migraciones..."
if alembic upgrade head; then
    echo "✅ Migraciones aplicadas con éxito."
else
    echo "⚠️  ADVERTENCIA: Las migraciones fallaron o ya estaban aplicadas."
    echo "Si el error es 'index already exists' o 'index does not exist', puedes ignorarlo si la DB ya tiene la estructura."
fi

# 4. Lanzar Aplicación
echo "🚀 Iniciando servidor..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000