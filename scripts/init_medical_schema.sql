CREATE SCHEMA IF NOT EXISTS medical;

CREATE TABLE IF NOT EXISTS medical.user_health_profile
(
    id         BIGSERIAL PRIMARY KEY,
    user_id    TEXT        NOT NULL REFERENCES public.users (identifier) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    first_name TEXT,
    last_name  TEXT,
    age        INTEGER,
    sex        CHAR(1) CHECK (sex IN ('M', 'F', 'X')), -- male, female, other
    height     NUMERIC(5, 2),                          -- cm
    weight     NUMERIC(5, 2),                          -- kg

    CONSTRAINT uq_user_health_profile_user_id UNIQUE (user_id)
);
