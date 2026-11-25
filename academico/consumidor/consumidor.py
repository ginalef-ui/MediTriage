import json
import os
import time

import psycopg
from kafka import KafkaConsumer
from kafka.structs import TopicPartition, OffsetAndMetadata


DATABASE_URL = os.environ["DATABASE_URL"]
KAFKA_SERVIDOR = os.environ.get("KAFKA_SERVIDOR", "kafka:19092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "meditriage.eventos")

NOMBRE_CONSUMIDOR = "meditriage-consumidor-demo"


def main():
    print("Consumidor de eventos iniciado.", flush=True)

    while True:
        consumidor = None

        try:
            consumidor = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=[KAFKA_SERVIDOR],
                group_id=NOMBRE_CONSUMIDOR,
                auto_offset_reset="earliest",
                enable_auto_commit=False,
                value_deserializer=lambda valor: json.loads(
                    valor.decode("utf-8")
                )
            )

            print("Conectado a Kafka. Esperando eventos...", flush=True)

            for mensaje in consumidor:
                evento = mensaje.value

                event_id = int(evento["event_id"])
                tipo = str(evento["tipo"])
                atencion_id = int(evento["atencion_id"])

                with psycopg.connect(DATABASE_URL) as conexion:
                    with conexion.cursor() as cursor:
                        cursor.execute(
                            """
                            INSERT INTO eventos_consumidos (
                                event_id,
                                consumidor,
                                tipo,
                                atencion_id
                            )
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (event_id, consumidor) DO NOTHING
                            RETURNING event_id
                            """,
                            (
                                event_id,
                                NOMBRE_CONSUMIDOR,
                                tipo,
                                atencion_id
                            )
                        )

                        nuevo = cursor.fetchone()

                # La transaccion de PostgreSQL ya se confirmo.
                # Ahora confirmamos la posicion del mensaje en Kafka.
                particion = TopicPartition(
                    mensaje.topic,
                    mensaje.partition
                )

                siguiente_offset = OffsetAndMetadata(
                    mensaje.offset + 1,
                    "",
                    -1
                )

                consumidor.commit(
                    offsets={particion: siguiente_offset}
                )

                if nuevo:
                    print(
                        "Evento procesado:",
                        event_id,
                        tipo,
                        flush=True
                    )
                else:
                    print(
                        "Evento duplicado omitido:",
                        event_id,
                        flush=True
                    )

        except Exception as error:
            print(
                "Error en consumidor; se reintentara:",
                str(error),
                flush=True
            )

            if consumidor is not None:
                try:
                    consumidor.close()
                except Exception:
                    pass

            time.sleep(5)


if __name__ == "__main__":
    main()