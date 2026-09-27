import logging
import os
import time
from pathlib import Path

from pipelines.heartbeat import record_worker_heartbeat

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("riverhacks.worker")

HEALTH_FILE = Path("/tmp/riverhacks-worker-heartbeat")


def run() -> None:
    interval = max(5, int(os.getenv("WORKER_INTERVAL_SECONDS", "30")))
    logger.info("worker started with a %s second interval", interval)

    while True:
        try:
            observed_at = record_worker_heartbeat()
            HEALTH_FILE.touch()
            logger.info("heartbeat recorded at %s", observed_at.isoformat())
        except Exception:
            logger.exception("worker cycle failed; retrying")

        time.sleep(interval)


if __name__ == "__main__":
    run()
