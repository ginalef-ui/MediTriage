# Bounded Contexts - MediTriage

## Contexto de Identidad

### Propósito

Gestionar la información personal de los pacientes y usuarios del sistema.

### Responsabilidades

- Registro de pacientes.
- Gestión de datos personales.
- Identificación de pacientes.
- Gestión de usuarios.

### Entidades principales

- Paciente
- Usuario
- Rol

### Eventos asociados

- patient.registered
- user.created
- user.updated

---

## Contexto de Triaje

### Propósito

Gestionar el proceso de clasificación inicial de pacientes según su nivel de urgencia.

### Responsabilidades

- Recepción de síntomas.
- Captura de signos vitales.
- Generación de clasificación asistida.
- Priorización de pacientes.

### Entidades principales

- TriageAssessment
- Symptoms
- VitalSigns

### Eventos asociados

- symptoms.reported
- vitals.captured
- triage.requested
- triage.completed
- triage.reclassified

---

## Contexto Clínico

### Propósito

Gestionar la información clínica utilizada por el personal médico durante la atención de pacientes.

### Responsabilidades

- Consulta de historial clínico.
- Registro de observaciones médicas.
- Seguimiento de atención.

### Entidades principales

- ClinicalRecord
- PatientHistory
- MedicalObservation

### Eventos asociados

- history.requested
- medical.note.created
- patient.attended

---

## Contexto de Auditoría

### Propósito

Mantener la trazabilidad de las acciones realizadas dentro del sistema.

### Responsabilidades

- Registro de eventos.
- Seguimiento de decisiones de IA.
- Auditoría de actividades.

### Entidades principales

- AuditLog
- AuditEvent

### Eventos asociados

- audit.recorded
- triage.audited
- access.logged

---

## Contexto de Notificaciones

### Propósito

Mantener informado al paciente durante el proceso de atención.

### Responsabilidades

- Notificaciones de espera.
- Alertas de reevaluación.
- Mensajes informativos.

### Entidades principales

- Notification
- Alert

### Eventos asociados

- notification.sent
- waiting.time.updated
- reevaluation.alert.triggered
