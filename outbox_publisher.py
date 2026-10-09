import os, time, json
import psycopg2
from psycopg2.extras import RealDictCursor
from kafka import KafkaProducer

def process_outbox():
    conn = psycopg2.connect(host="localhost", dbname="meditriage_db", user="meditriage_user", password="meditriage_password")
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    print("Outbox Relay Worker iniciado...")
    while True:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, aggregate_id, event_type, payload FROM outbox_events WHERE status = 'PENDING' FOR UPDATE SKIP LOCKED;")
                pending = cur.fetchall()

                for event in pending:
                    producer.send("meditriage.events", key=event['aggregate_id'].encode('utf-8'), value=event['payload'])
                    cur.execute("UPDATE outbox_events SET status = 'PUBLISHED', processed_at = CURRENT_TIMESTAMP WHERE id = %s;", (str(event['id']),))
                
                conn.commit()
                if not pending: time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            conn.rollback()
            time.sleep(2)

if __name__ == "__main__":
    process_outbox()
