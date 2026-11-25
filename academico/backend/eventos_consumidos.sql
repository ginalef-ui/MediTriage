CREATE TABLE IF NOT EXISTS eventos_consumidos (
    event_id BIGINT NOT NULL,
    consumidor VARCHAR(100) NOT NULL,
    tipo VARCHAR(60) NOT NULL,
    atencion_id BIGINT NOT NULL,
    fecha_procesamiento TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (event_id, consumidor)
);