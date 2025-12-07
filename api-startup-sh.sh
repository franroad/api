#!/bin/bash

# exec para que quede como proceso principal
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
