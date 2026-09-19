#!/bin/bash
set -e # If there is any issue the script is aborted and throws an error
       # If not specified the script keeps runing and the failure is not advertised


echo "Waiting for postgres container..."
until pg_isready -h "$DDBB_HOSTNAME" -p "$DDBB_PORT"; do
  sleep 1
done

echo "Postgres is good to go!"

# exec para que quede como proceso principal
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
