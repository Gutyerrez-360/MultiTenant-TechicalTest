#!/bin/sh
set -e

echo "Ejecutando migraciones Alembic..."
alembic upgrade head

echo "Iniciando FastAPI..."
exec uvicorn multiTenantApi.main:app --host 0.0.0.0 --port 8000
