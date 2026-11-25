BEGIN;

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS intervencion_inmediata BOOLEAN;

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS situacion_alto_riesgo BOOLEAN;

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS alteracion_conciencia_nueva BOOLEAN;

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS dolor_o_malestar_intenso BOOLEAN;

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS recursos_previstos INTEGER
        CHECK (recursos_previstos BETWEEN 0 AND 2);

COMMIT;