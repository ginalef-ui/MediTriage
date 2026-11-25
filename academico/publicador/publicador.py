import json
import os
import time

import psycopg
from psycopg.rows import dict_row
from kafka import KafkaProducer


DATABASE_URL = os.environ["DATABASE_URL"]
KAFKA_SERVIDOR = os.environ.get("KAFKA_SERVIDOR", "kafka:19092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "meditriage.eventos")


def main():
    productor = None

    print("Publicador de eventos iniciado.", flush=True)

    while True:
        try:
            if productor is None:
                productor = KafkaProducer(
                    bootstrap_servers=[KAFKA_SERVIDOR],
                    acks="all",
                    retries=3,
                    request_timeout_ms=10000,
                    max_block_ms=10000
                )

                print("Conexion con Kafka establecida.", flush=True)

            with psycopg.connect(
                DATABASE_URL,
                row_factory=dict_row
            ) as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id, tipo, atencion_id, datos, fecha_creacion
                        FROM eventos_pendientes
                        WHERE estado = 'pendiente'
                        ORDER BY id
                        FOR UPDATE SKIP LOCKED
                        LIMIT 1
                        """
                    )

                    evento = cursor.fetchone()

                    if evento is not None:
                        mensaje = {
                            "event_id": str(evento["id"]),
                            "tipo": evento["tipo"],
                            "atencion_id": evento["atencion_id"],
                            "datos": evento["datos"],
                            "fecha_creacion": (
                                evento["fecha_creacion"].isoformat()
                            )
                        }

                        resultado = productor.send(
                            KAFKA_TOPIC,
                            key=str(evento["atencion_id"]).encode("utf-8"),
                            value=json.dumps(
                                mensaje,
                                ensure_ascii=False
                            ).encode("utf-8")
                        )

                        # Esperar confirmacion antes de actualizar PostgreSQL.
                        resultado.get(timeout=20)

                        cursor.execute(
                            """
                            UPDATE eventos_pendientes
                            SET estado = 'publicado',
                                fecha_publicacion = CURRENT_TIMESTAMP
                            WHERE id = %s
                            """,
                            (evento["id"],)
                        )

            if evento is not None:
                print(
                    "Evento publicado:",
                    mensaje["event_id"],
                    mensaje["tipo"],
                    flush=True
                )
            else:
                time.sleep(2)

        except Exception as error:
            print(
                "Error al publicar; se reintentara:",
                str(error),
                flush=True
            )

            if productor is not None:
                try:
                    productor.close(timeout=5)
                except Exception:
                    pass

                productor = None

            time.sleep(5)


if __name__ == "__main__":
    main()