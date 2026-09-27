# RiverHacks 2026

Portable four-service application stack for RiverHacks 2026:

- `frontend`: static demo UI and reverse proxy
- `api`: FastAPI HTTP service
- `worker`: independent Python pipeline process
- `postgres`: one persistent PostgreSQL server

The API and worker are separate processes so long-running pipeline work cannot
block HTTP requests. Both share the same PostgreSQL instance, with logical
separation provided by the `app` and `pipeline` schemas.

## Run locally

1. Copy `.env.example` to `.env`.
2. Replace `POSTGRES_PASSWORD` with a strong local value.
3. Start the stack:

   ```bash
   docker compose up --build
   ```

4. Open <http://localhost:8080>.

The frontend proxies API requests under `/api`, including the interactive API
documentation at <http://localhost:8080/api/docs>.

Stop the containers without deleting PostgreSQL data:

```bash
docker compose down
```

To also remove the local database volume, explicitly run
`docker compose down --volumes`.

## Repository layout

```text
app/                    FastAPI application
database/init/          first-boot PostgreSQL schema
frontend/               static UI and nginx reverse proxy
pipelines/              reusable worker jobs
shared/                 Python code shared by API and worker
worker/                 independent pipeline runtime
compose.yml             portable deployment contract
Dockerfile              API image (also preserves direct Coolify deployment)
```

## Deployment notes

- Deploy `compose.yml` as a Docker Compose resource in Coolify.
- Set the values from `.env.example` in Coolify's environment settings; never
  commit a real `.env` file.
- Persist the `postgres-data` named volume.
- Only the frontend publishes a host port. The API, worker, and database stay
  on the internal Compose network.
- Files in `database/init/` run only when PostgreSQL starts with a new, empty
  data volume. Use versioned migrations once the schema begins changing.

The root `Dockerfile` still builds the API by itself so the existing Coolify
application can keep running while the deployment is migrated to Compose.
