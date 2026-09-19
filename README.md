#  Project Name
Short description of what the project does and why it exists.

---

##  Overview
A concise explanation of the system, its purpose, and the main problems it solves.

---



##  Architecture Diagram
> Add your diagram here (Mermaid, PNG, or external link)


## Technologies used
- Docker & Docker compose
- Github & Github actions
- Helm
- Sops
- PostgreSql
- MinIO
- CloudNativePG
- Python: Fast api  and Pytest
- Flux CD

Next steps: 
- setup Helm and sops
- Setup 

## Environment Variables Documentation

## PostgreSQL Service

| Variable | Description | Required | Default | Example |
| :--- | :--- | :---: | :---: | :--- |
| `POSTGRES_USER` | Superuser username | No | `postgres` | `admin_user` |
| `POSTGRES_PASSWORD` | Superuser password | **Yes** | — | `super_secret_pass` |
| `POSTGRES_DB` | Default database created on startup | No | `POSTGRES_USER` | `app_db` |
| `PGDATA` | Location for database storage inside container | No | `/var/lib/postgresql/data/pgdata` | `/var/lib/postgresql/data/pgdata` |

---

## FastAPI Service

| Variable | Description | Required | Default | Example |
| :--- | :--- | :---: | :---: | :--- |
| `ENV` | Application environment (`development`, `staging`, `production`) | No | `development` | `production` |
| `PORT` | Container internal port | No | `8000` | `8000` |
| `DB_HOST` | Hostname/Service name of the PostgreSQL container | **Yes** | — | `postgres` |
| `DB_PORT` | PostgreSQL connection port | No | `5432` | `5432` |
| `DB_USER` | Username used by FastAPI to connect to Postgres | **Yes** | — | `admin_user` |
| `DB_PASSWORD` | Password used by FastAPI to connect to Postgres | **Yes** | — | `super_secret_pass` |
| `DB_NAME` | PostgreSQL database name | **Yes** | — | `app_db` |
| `SECRET_KEY` | JWT/Session signing secret | **Yes** | — | `09d25e094faa6ca2556...` |