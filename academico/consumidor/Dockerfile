FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    "psycopg[binary]==3.2.9" \
    "kafka-python==2.2.15"

COPY academico/consumidor/consumidor.py .

CMD ["python", "-u", "consumidor.py"]