#!/bin/sh
set -e
# exit on error

# Esperar a que la base de datos esté lista, usar lavariables definidas en .env
until pg_isready -h "$DDBB_HOSTNAME" -p 5432 -U "$DDBB_USER"; do
  echo "Esperando a la base de datos..."
  sleep 2
done

# Aplicar migraciones
alembic upgrade head

# Arrancar la API exec para que quede como proceso principal
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
