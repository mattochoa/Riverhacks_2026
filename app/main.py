from fastapi import FastAPI

app = FastAPI(
    title="RiverHacks 2026",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "RiverHacks 2026",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
