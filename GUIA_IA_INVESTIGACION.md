# MediTriage: integración de IA para investigación

## Alcance

Esta versión es exclusivamente para investigación con casos ficticios.

- El motor `esi_investigacion.py` es una implementación parcial de
  investigación basada en ESI v4. No está validado clínicamente.
- Las pruebas automatizadas comprueban comportamientos del código;
  no demuestran seguridad ni precisión clínica.
- El botón de sugerencia numérica de IA está pausado.
- La ruta de extracción de texto es experimental. Sus resultados deben
  ser revisados por una persona y no se usan automáticamente para triaje.
- No utilizar para pacientes reales ni para ordenar una cola clínica.

## Base de datos nueva

Primero seguir las instrucciones de README_ACADEMICO.md para iniciar
PostgreSQL y ejecutar, en este orden:

1. schema.sql
2. usuarios.sql
3. eventos.sql
4. eventos_consumidos.sql

Después ejecutar estas migraciones adicionales, también en orden:

5. sugerencias_ia.sql
6. decision_ia.sql
7. datos_triaje.sql
8. evaluacion_profesional.sql

Ejemplo para cada migración, desde la carpeta principal del proyecto:

Get-Content -Raw "academico\backend\sugerencias_ia.sql" | docker exec -i meditriage-academico-db psql -U meditriage -d meditriage -v ON_ERROR_STOP=1

Repetir el comando cambiando el nombre del archivo, respetando el orden.
Si alguna migración falla, detenerse y revisar el error antes de continuar.

## Kafka

Con Kafka iniciado, crear el topic:

docker exec meditriage-academico-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:19092 --create --if-not-exists --topic meditriage.eventos --partitions 1 --replication-factor 1

Si Kafka no inicia por permisos de su volumen, revisar sus logs y la
propiedad del volumen antes de cambiarla. No borrar volúmenes para resolverlo.

## Ollama

El endpoint experimental de extracción utiliza, actualmente:

qwen2.5:1.5b-instruct

Durante la investigación también se probó manualmente:

qwen2.5:3b-instruct

La versión 3B tiene una licencia de Qwen para investigación que debe
revisarse antes de otros usos. Ninguno de estos modelos se considera
validado clínicamente por este proyecto.

El backend de Docker consulta Ollama en host.docker.internal:11434.
El resultado de extracción puede contener omisiones, negaciones mal
interpretadas o evidencia no literal. No se utiliza automáticamente
para asignar una prioridad.

## Ejecutar pruebas del motor

Desde academico\backend:

py -m unittest test_esi_investigacion test_esi_recursos test_esi_signos test_esi_alcance -v

Estas pruebas no sustituyen una revisión de la implementación ni una
evaluación independiente con profesionales y casos de referencia.