BEGIN;

CREATE TABLE IF NOT EXISTS pacientes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    identificador VARCHAR(40) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS atenciones (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    paciente_id BIGINT NOT NULL
        REFERENCES pacientes(id),

    sintomas TEXT NOT NULL,
    pulsaciones INTEGER NOT NULL
        CHECK (pulsaciones BETWEEN 1 AND 250),

    presion_arterial VARCHAR(7) NOT NULL,

    prioridad_confirmada INTEGER
        CHECK (prioridad_confirmada BETWEEN 1 AND 5),

    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente', 'esperando', 'atendido')),

    motivo_cambio TEXT,
    fecha_registro TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_confirmacion TIMESTAMPTZ,
    fecha_atencion TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_atenciones_paciente
    ON atenciones(paciente_id);

COMMIT;