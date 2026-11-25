# MediTriage: versión académica

Esta versión demuestra el flujo de MediTriage con datos ficticios.

## Funciones

- Inicio de sesión con roles de prueba.
- Registro de pacientes y atenciones ficticias.
- Confirmación manual de prioridad y cola de espera.
- Historial de atenciones.
- Publicación y consumo de eventos mediante PostgreSQL y Kafka.
- Detección de eventos duplicados por el consumidor.

## Límites de la demo

- Usar únicamente datos ficticios.
- La prioridad se selecciona manualmente; no hay IA conectada.
- No es un sistema clínico validado ni apto para producción.
- Las cuentas y contraseñas incluidas son de prueba.
- Los servicios están pensados para ejecutarse localmente.

## Requisitos

- Docker Desktop y Docker Compose.
- Git, si se obtiene el proyecto desde el repositorio.

## Archivos principales

- academico/backend: API, panel y scripts SQL.
- academico/publicador: envía eventos pendientes a Kafka.
- academico/consumidor: procesa eventos y detecta duplicados.
- docker-compose.*.yml: configuración de los servicios.

## Primera configuración de la base de datos

En PowerShell, desde la carpeta principal del proyecto, iniciar PostgreSQL:

docker compose -f docker-compose.academico.yml up -d postgres

Esperar a que el contenedor de PostgreSQL esté funcionando. Luego ejecutar,
en este orden, los scripts SQL:

Get-Content -Raw "academico\backend\schema.sql" | docker exec -i meditriage-academico-db psql -U meditriage -d meditriage -v ON_ERROR_STOP=1

Get-Content -Raw "academico\backend\usuarios.sql" | docker exec -i meditriage-academico-db psql -U meditriage -d meditriage -v ON_ERROR_STOP=1

Get-Content -Raw "academico\backend\eventos.sql" | docker exec -i meditriage-academico-db psql -U meditriage -d meditriage -v ON_ERROR_STOP=1

Get-Content -Raw "academico\backend\eventos_consumidos.sql" | docker exec -i meditriage-academico-db psql -U meditriage -d meditriage -v ON_ERROR_STOP=1

## Iniciar todos los servicios

docker compose -f docker-compose.academico.yml -f docker-compose.backend.yml -f docker-compose.kafka.yml -f docker-compose.publicador.yml -f docker-compose.consumidor.yml up -d --build

El publicador y el consumidor reintentan la conexión mientras Kafka inicia.
El topic meditriage.eventos debe existir en Kafka antes de realizar la prueba.
La primera configuración de Kafka puede requerir ajustar los permisos de su
volumen, según el entorno de Docker.

## Abrir el panel

http://127.0.0.1:8000/panel

Cuentas de prueba: admision, triaje, medico y admin.
Contraseña inicial de demostración: Demo2026!

## Datos y volúmenes

PostgreSQL y Kafka guardan sus datos en volúmenes Docker. Esos datos no están
incluidos en el repositorio. Una copia nueva comienza con una base separada
y debe configurarse con los scripts indicados arriba.

No levantar simultáneamente dos copias de esta configuración sin antes
resolver los posibles conflictos de nombres de contenedores y puertos.