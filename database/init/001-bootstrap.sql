CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS pipeline;

CREATE TABLE IF NOT EXISTS app.service_heartbeats (
    service_name text PRIMARY KEY,
    last_seen timestamptz NOT NULL,
    details jsonb NOT NULL DEFAULT '{}'::jsonb
);
