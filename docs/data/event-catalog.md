# Catálogo de Eventos de Dominio - MediTriage

A continuación se detallan 12 eventos del ciclo de vida principal del paciente en el sistema MediTriage. Todos los eventos son inmutables e incluyen un `trace_id` para garantizar la auditoría y trazabilidad en toda la arquitectura event-driven.

### 1. paciente.registrado
* **Descripción:** Un nuevo paciente ha sido registrado en el sistema con su RUT validado y consentimiento firmado.
* **Versión:** 1.0
* **Productor:** Contexto de Identidad
* **Consumidores:** Contexto Clínico, Contexto de Auditoría
* **Campos:** `event_id`, `trace_id`, `RUT`, `nombre`, `timestamp`

### 2. encounter.started
* **Descripción:** Se inicia un nuevo encuentro clínico (atención de urgencia) vinculado al paciente.
* **Versión:** 1.0
* **Productor:** Contexto Clínico (Encounter)
* **Consumidores:** Base de Datos PostgreSQL
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `RUT`, `timestamp`

### 3. sintomas.reportados
* **Descripción:** El paciente completa el formulario digital reportando sus síntomas.
* **Versión:** 1.0
* **Productor:** Contexto Clínico (Frontend Paciente)
* **Consumidores:** Motor IA, Contexto de Auditoría
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `Sintomas`, `timestamp`

### 4. vitals.captured
* **Descripción:** La enfermera ingresa las mediciones de los signos vitales del paciente.
* **Versión:** 1.0
* **Productor:** Contexto Clínico (Enfermera)
* **Consumidores:** Motor IA
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `SignosVitales` (Pulsaciones, PresionSanguinea), `timestamp`

### 5. triage.requested
* **Descripción:** El comando envía el caso consolidado al motor IA para su evaluación.
* **Versión:** 1.0
* **Productor:** Contexto Clínico
* **Consumidores:** Motor IA (Azure Machine Learning)
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `RUT`, `Sintomas`, `SignosVitales`, `timestamp`

### 6. triage.completed
* **Descripción:** El motor IA evalúa los datos y devuelve una categoría sugerida junto con su razonamiento.
* **Versión:** 1.0
* **Productor:** Motor IA
* **Consumidores:** Contexto Clínico, Contexto de Auditoría (Azure SQL Ledger)
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `nivelEsi` (1 al 5), `justificacionAi`, `timestamp`

### 7. triage.confirmed
* **Descripción:** La enfermera aprueba la categoría ESI sugerida por la IA sin modificaciones.
* **Versión:** 1.0
* **Productor:** Contexto Clínico (Enfermera)
* **Consumidores:** Redis (Tablero de Sala de Espera), Contexto de Auditoría
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `nivelEsiConfirmado`, `enfermera_id`, `timestamp`

### 8. triage.modified
* **Descripción:** La enfermera descarta la sugerencia de la IA y modifica la categoría ESI según su criterio.
* **Versión:** 1.0
* **Productor:** Contexto Clínico (Enfermera)
* **Consumidores:** Redis (Tablero de Sala de Espera), Contexto de Auditoría
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `nivelEsiOriginal`, `nivelEsiNuevo`, `motivoModificacion`, `enfermera_id`, `timestamp`

### 9. paciente.cola
* **Descripción:** El paciente entra oficialmente a la cola de prioridad de la sala de espera.
* **Versión:** 1.0
* **Productor:** Contexto Clínico
* **Consumidores:** Redis (Frontend Enfermera / Sala de Espera)
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `nivelEsi`, `estado` ("WAITING"), `timestamp`

### 10. paciente.llamado
* **Descripción:** El médico llama al paciente desde el tablero dinámico a su box de atención.
* **Versión:** 1.0
* **Productor:** Contexto Clínico (Médico)
* **Consumidores:** Pantallas de Sala de Espera
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `medico_id`, `boxAsignado`, `timestamp`

### 11. historial.visto
* **Descripción:** El médico visualiza el historial clínico previo del paciente.
* **Versión:** 1.0
* **Productor:** Contexto Clínico (Médico)
* **Consumidores:** Contexto de Auditoría
* **Campos:** `event_id`, `trace_id`, `RUT`, `medico_id`, `timestamp`

### 12. paciente.atendido
* **Descripción:** Finaliza la atención médica de urgencia del paciente.
* **Versión:** 1.0
* **Productor:** Contexto Clínico (Médico)
* **Consumidores:** Base de Datos PostgreSQL (Update Encounter State), Tablero de Sala de Espera
* **Campos:** `event_id`, `trace_id`, `encounter_id`, `estado` ("ATTENDED"), `timestamp`
