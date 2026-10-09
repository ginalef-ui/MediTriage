import json, psycopg2
from kafka import KafkaConsumer

def run_consumer():
    conn = psycopg2.connect(host="localhost", dbname="meditriage_db", user="meditriage_user", password="meditriage_password")
    consumer = KafkaConsumer("meditriage.events", bootstrap_servers=['localhost:9092'], group_id="clinica-group", value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    print("Consumidor escuchando eventos...")
    for message in consumer:
        event = message.value
        event_id = event.get("event_id")

        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM processed_events WHERE event_id = %s;", (event_id,))
            if cur.fetchone():
                print(f"Evento {event_id} omitido (Idempotencia).")
                continue

            print(f"Procesando Evento: {event}")
            cur.execute("INSERT INTO processed_events (event_id, consumer_name) VALUES (%s, 'clinica-group');", (event_id,))
            conn.commit()

if __name__ == "__main__":
    run_consumer()
