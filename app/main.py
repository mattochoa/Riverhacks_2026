import os

from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row

from shared.database import connect

app = FastAPI(
    title="RiverHacks 2026",
    version="0.1.0",
    root_path=os.getenv("ROOT_PATH", ""),
)


@app.get("/")
def root():
    return {
        "name": "RiverHacks 2026",
        "environment": os.getenv("APP_ENV", "development"),
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    try:
        with connect() as connection:
            connection.execute("SELECT 1")
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc

    return {"status": "ready"}


@app.get("/heartbeats")
def heartbeats():
    try:
        with connect(row_factory=dict_row) as connection:
            rows = connection.execute(
                """
                SELECT service_name, last_seen, details
                FROM app.service_heartbeats
                ORDER BY service_name
                """
            ).fetchall()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc

    return {"services": rows}
