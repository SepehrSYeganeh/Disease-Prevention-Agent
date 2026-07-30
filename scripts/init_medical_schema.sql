CREATE SCHEMA IF NOT EXISTS medical;

CREATE TABLE medical.user_health_profile
(
    id                       UUID PRIMARY KEY     DEFAULT gen_random_uuid(),
    user_id                  UUID        NOT NULL UNIQUE REFERENCES public.users (id) ON DELETE CASCADE,

    first_name               TEXT,
    last_name                TEXT,
    birthdate                DATE,
    sex                      CHAR(1) CHECK (sex IN ('M', 'F', 'X')), -- male, female, other
    is_pregnant              BOOLEAN,

    personal_medical_history JSONB,                                  -- chronic conditions, surgeries, allergies, vaccinations, diagnoses
    family_medical_history   JSONB,                                  -- hereditary conditions in first-degree relatives
    lifestyle_habits         JSONB,                                  -- diet, physical activity, sleep
    substance_use            JSONB,                                  -- smoking, alcohol, recreational drugs
    psychiatric_disorders    JSONB,                                  -- stress level, depression/anxiety history
    medications_supplements  JSONB,                                  -- prescriptions, OTC, vitamins, herbal
    clinical_data            JSONB,                                  -- recent lab results

    created_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE medical.user_biometric_log
(
    id            UUID PRIMARY KEY     DEFAULT gen_random_uuid(),
    user_id       UUID        NOT NULL REFERENCES public.users (id) ON DELETE CASCADE,
    recorded_at   TIMESTAMPTZ NOT NULL DEFAULT now() CHECK (recorded_at <= now()),
    height_cm     NUMERIC(5, 2) CHECK (height_cm IS NULL OR height_cm > 0),
    weight_kg     NUMERIC(5, 2) CHECK (weight_kg IS NULL OR weight_kg > 0),
    bmi           NUMERIC(5, 2) GENERATED ALWAYS AS (
        CASE
            WHEN height_cm IS NOT NULL AND weight_kg IS NOT NULL AND height_cm > 0
                THEN weight_kg / ((height_cm / 100) ^ 2)
            END
        ) STORED,
    systolic_bp   SMALLINT,
    diastolic_bp  SMALLINT,
    resting_hr    SMALLINT,
    blood_glucose NUMERIC(5, 1) CHECK (blood_glucose IS NULL OR blood_glucose > 0), -- mg/dL
    triglycerides NUMERIC(5, 1) CHECK (triglycerides IS NULL OR triglycerides > 0),
    notes         JSONB
);

CREATE INDEX idx_biometric_user_time ON medical.user_biometric_log (user_id, recorded_at DESC);
