FROM python:3.12-slim

WORKDIR /app

COPY academico/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY academico/backend/main.py academico/backend/panel.html ./

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]