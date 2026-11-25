BEGIN;

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS confirmado_por BIGINT
        REFERENCES usuarios(id);

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS sugerencia_utilizada_id BIGINT
        REFERENCES sugerencias_ia(id);

COMMIT;