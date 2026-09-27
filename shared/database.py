import os
from collections.abc import Callable
from typing import Any

import psycopg


def connection_parameters() -> dict[str, Any]:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return {"conninfo": database_url}

    return {
        "host": os.getenv("DB_HOST", "postgres"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("POSTGRES_DB", "riverhacks"),
        "user": os.getenv("POSTGRES_USER", "riverhacks"),
        "password": os.getenv("POSTGRES_PASSWORD", ""),
    }


def connect(*, row_factory: Callable[..., Any] | None = None):
    parameters = connection_parameters()
    if row_factory is not None:
        parameters["row_factory"] = row_factory
    return psycopg.connect(**parameters)
