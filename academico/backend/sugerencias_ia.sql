CREATE TABLE IF NOT EXISTS sugerencias_ia (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    atencion_id BIGINT NOT NULL
        REFERENCES atenciones(id),

    usuario_id BIGINT NOT NULL
        REFERENCES usuarios(id),

    modelo VARCHAR(100) NOT NULL,

    prioridad_sugerida INTEGER NOT NULL
        CHECK (prioridad_sugerida BETWEEN 1 AND 5),

    explicacion TEXT NOT NULL,

    fecha_creacion TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_sugerencias_ia_atencion
    ON sugerencias_ia(atencion_id, fecha_creacion DESC);