FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY worker/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN addgroup --system riverhacks \
    && adduser --system --ingroup riverhacks riverhacks

COPY worker ./worker
COPY pipelines ./pipelines
COPY shared ./shared

USER riverhacks

CMD ["python", "-m", "worker.main"]
