BEGIN;

CREATE TABLE IF NOT EXISTS eventos_pendientes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    tipo VARCHAR(60) NOT NULL,

    atencion_id BIGINT NOT NULL
        REFERENCES atenciones(id),

    datos JSONB NOT NULL,

    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente', 'publicado')),

    fecha_creacion TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_publicacion TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_eventos_pendientes_estado
    ON eventos_pendientes(estado, id);


CREATE OR REPLACE FUNCTION registrar_evento_atencion()
RETURNS TRIGGER AS $$
DECLARE
    tipo_evento TEXT;
BEGIN
    IF TG_OP = 'INSERT' THEN
        tipo_evento := 'atencion.registrada';

    ELSIF TG_OP = 'UPDATE'
          AND OLD.estado IS DISTINCT FROM NEW.estado THEN

        IF NEW.estado = 'esperando' THEN
            tipo_evento := 'triaje.confirmado';

        ELSIF NEW.estado = 'atendido' THEN
            tipo_evento := 'atencion.finalizada';
        END IF;
    END IF;

    IF tipo_evento IS NOT NULL THEN
        INSERT INTO eventos_pendientes (
            tipo,
            atencion_id,
            datos
        )
        VALUES (
            tipo_evento,
            NEW.id,
            jsonb_build_object(
                'atencion_id', NEW.id,
                'estado', NEW.estado
            )
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS trigger_evento_atencion_insert
    ON atenciones;

CREATE TRIGGER trigger_evento_atencion_insert
AFTER INSERT ON atenciones
FOR EACH ROW
EXECUTE FUNCTION registrar_evento_atencion();


DROP TRIGGER IF EXISTS trigger_evento_atencion_estado
    ON atenciones;

CREATE TRIGGER trigger_evento_atencion_estado
AFTER UPDATE OF estado ON atenciones
FOR EACH ROW
EXECUTE FUNCTION registrar_evento_atencion();

COMMIT;