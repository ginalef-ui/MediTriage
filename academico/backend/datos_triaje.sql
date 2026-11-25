BEGIN;

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS edad_anos INTEGER
        CHECK (edad_anos BETWEEN 0 AND 120);

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS frecuencia_respiratoria INTEGER
        CHECK (frecuencia_respiratoria BETWEEN 1 AND 100);

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS saturacion_oxigeno INTEGER
        CHECK (saturacion_oxigeno BETWEEN 1 AND 100);

ALTER TABLE atenciones
    ADD COLUMN IF NOT EXISTS temperatura NUMERIC(4,1)
        CHECK (temperatura BETWEEN 25 AND 45);

COMMIT;