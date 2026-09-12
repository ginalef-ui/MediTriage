# Trazabilidad S02 → S03
## Proyecto: MediTriage

Esta trazabilidad permite relacionar los requisitos definidos en la fase de Ingeniería de Requisitos (S02) con los componentes arquitectónicos definidos en la fase de Arquitectura de Software (S03).

---

## US-01: Registro de síntomas del paciente

### S02

Actor:
- Paciente

Impacto:
- Entregar información relevante de salud antes de ser atendido.

Deliverable:
- Formulario digital de registro de pacientes y síntomas.

### S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Base de Datos

Justificación:
Permite registrar, validar y almacenar los síntomas ingresados por el paciente.

---

## US-02: Visualización de prioridad de pacientes (Clasificación asistida)

### S02

Actor:
- Enfermera

Impacto:
- Priorizar pacientes de manera rápida y eficiente.

Deliverable:
- Sistema de clasificación asistida.

### S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Motor de Clasificación IA

Justificación:
Permite generar y visualizar la prioridad asignada a cada paciente.

---

## US-03: Consulta de historial clínico

### S02

Actor:
- Médico

Impacto:
- Acceder rápidamente a la información clínica del paciente.

Deliverable:
- Historial clínico digital.

### S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Base de Datos

Justificación:
Permite consultar antecedentes clínicos y clasificaciones previas.

---

## US-04: Auditoría y revisión de registros clínicos

### S02

Actor:
- Auditor Clínico

Impacto:
- Supervisar y validar la calidad del proceso de clasificación.

Deliverable:
- Módulo de auditoría y revisión clínica.

### S03

Contenedores relacionados:
- Backend API
- Base de Datos

Justificación:
Permite revisar registros históricos y verificar decisiones tomadas por el sistema.

---

## US-05: Panel de administración y permisos

### S02

Actor:
- Administrador

Impacto:
- Garantizar el correcto funcionamiento y seguridad del sistema.

Deliverable:
- Panel de administración de usuarios y permisos.

### S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Base de Datos

Justificación:
Permite gestionar usuarios, perfiles, roles y permisos de acceso.

---

## US-06: Notificación de estado de espera en tiempo real

### S02

Actor:
- Paciente

Impacto:
- Mantener informado al paciente durante la espera.

Deliverable:
- Sistema de notificaciones.

### S03

Contenedores relacionados:
- Frontend Web
- Backend API

Justificación:
Permite comunicar al paciente el tiempo estimado de espera y cambios en su estado.

---

## US-07: Reevaluación automática por tiempo de espera excedido

### S02

Actor:
- Enfermera

Impacto:
- Detectar pacientes que requieren reevaluación.

Deliverable:
- Sistema de alertas.

### S03

Contenedores relacionados:
- Backend API
- Motor de Clasificación IA
- Base de Datos

Justificación:
Permite generar alertas cuando un paciente supera los tiempos máximos de espera establecidos.

---

## US-08: Autenticación de doble factor

### S02

Actor:
- Administrador

Impacto:
- Aumentar la seguridad de acceso al sistema.

Deliverable:
- Sistema de autenticación reforzada.

### S03

Contenedores relacionados:
- Frontend Web
- Backend API

Justificación:
Permite implementar autenticación de dos factores para proteger la información clínica.

---

## US-09: Registro y categorización de cancelaciones voluntarias

### S02

Actor:
- Enfermera

Impacto:
- Mantener actualizada la lista de pacientes en espera.

Deliverable:
- Registro de cancelaciones.

### S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Base de Datos

Justificación:
Permite registrar y almacenar las cancelaciones de atención realizadas por los pacientes.

---

## US-10: Selección de idioma en el formulario del paciente

### S02

Actor:
- Paciente

Impacto:
- Mejorar la accesibilidad del sistema.

Deliverable:
- Formulario multilenguaje.

### S03

Contenedores relacionados:
- Frontend Web

Justificación:
Permite adaptar la interfaz de usuario a distintos idiomas de forma dinámica.
