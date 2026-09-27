from datetime import datetime, timezone

from psycopg.types.json import Jsonb

from shared.database import connect


def record_worker_heartbeat() -> datetime:
    observed_at = datetime.now(timezone.utc)

    with connect() as connection:
        connection.execute(
            """
            INSERT INTO app.service_heartbeats (service_name, last_seen, details)
            VALUES (%s, %s, %s)
            ON CONFLICT (service_name)
            DO UPDATE SET last_seen = EXCLUDED.last_seen,
                          details = EXCLUDED.details
            """,
            (
                "worker",
                observed_at,
                Jsonb({"state": "running"}),
            ),
        )
        connection.commit()

    return observed_at
