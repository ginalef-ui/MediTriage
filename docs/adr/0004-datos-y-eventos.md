# ADR 0004: Selección de Motores de Datos y Broker de Eventos

## Contexto
MediTriage requiere procesar el ciclo de vida de los pacientes de forma asíncrona, manteniendo la consistencia entre el registro clínico y las proyecciones de lectura (CQRS).

## Decisión
- **Broker de Eventos:** Apache Kafka. Justificación: Permite alto throughput, persistencia de eventos (log distribuido) y replay de eventos clínicos.
- **Base de Datos Principal:** PostgreSQL. Justificación: Garantiza transacciones ACID para el estado actual de los triajes (Encounter).
- **Patrón de Consistencia:** Outbox Pattern. Justificación: Guardamos el evento en la misma transacción de BD que la entidad clínica para evitar pérdida de mensajes si el broker falla.
