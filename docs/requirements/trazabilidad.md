# Trazabilidad S02 → S04
## Proyecto: MediTriage

Este documento permite relacionar los requisitos definidos en la fase de Ingeniería de Requisitos (S02), la arquitectura definida en la fase de Arquitectura de Software (S03) y las decisiones cloud adoptadas en la fase de Diseño para la Nube (S04).

---

# US-01: Registro de síntomas del paciente

## S02

Actor:
- Paciente

Impacto:
- Entregar información relevante de salud antes de ser atendido.

Deliverable:
- Formulario digital de registro de pacientes y síntomas.

## S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Base de Datos

Justificación:
Permite registrar, validar y almacenar los síntomas ingresados por el paciente.

## S04

Servicios Cloud:
- Azure Container Apps
- Azure Database for PostgreSQL

Justificación:
Permiten desplegar la aplicación y almacenar la información clínica de forma gestionada.

---

# US-02: Visualización de prioridad de pacientes (Clasificación asistida)

## S02

Actor:
- Enfermera

Impacto:
- Priorizar pacientes de manera rápida y eficiente.

Deliverable:
- Sistema de clasificación asistida.

## S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Motor de Clasificación IA

Justificación:
Permite generar y visualizar la prioridad asignada a cada paciente.

## S04

Servicios Cloud:
- Azure Container Apps
- Azure Machine Learning

Justificación:
Permiten ejecutar y desplegar el motor de clasificación asistida basado en IA.

---

# US-03: Consulta de historial clínico

## S02

Actor:
- Médico

Impacto:
- Acceder rápidamente a la información clínica del paciente.

Deliverable:
- Historial clínico digital.

## S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Base de Datos

Justificación:
Permite consultar antecedentes clínicos y clasificaciones previas.

## S04

Servicios Cloud:
- Azure Container Apps
- Azure Database for PostgreSQL

Justificación:
Permiten acceder y almacenar historiales clínicos de forma segura.

---

# US-04: Auditoría y revisión de registros clínicos

## S02

Actor:
- Auditor Clínico

Impacto:
- Supervisar y validar la calidad del proceso de clasificación.

Deliverable:
- Módulo de auditoría y revisión clínica.

## S03

Contenedores relacionados:
- Backend API
- Base de Datos

Justificación:
Permite revisar registros históricos y verificar decisiones tomadas por el sistema.

## S04

Servicios Cloud:
- Azure SQL Database Ledger

Justificación:
Permite registrar eventos inmutables y verificables para auditoría.

---

# US-05: Panel de administración y permisos

## S02

Actor:
- Administrador

Impacto:
- Garantizar el correcto funcionamiento y seguridad del sistema.

Deliverable:
- Panel de administración de usuarios y permisos.

## S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Base de Datos

Justificación:
Permite gestionar usuarios, perfiles, roles y permisos de acceso.

## S04

Servicios Cloud:
- Azure Container Apps
- Azure Database for PostgreSQL

Justificación:
Permiten administrar usuarios y proteger la información operativa.

---

# US-06: Notificación de estado de espera en tiempo real

## S02

Actor:
- Paciente

Impacto:
- Mantener informado al paciente durante la espera.

Deliverable:
- Sistema de notificaciones.

## S03

Contenedores relacionados:
- Frontend Web
- Backend API

Justificación:
Permite comunicar al paciente el tiempo estimado de espera y cambios en su estado.

## S04

Servicios Cloud:
- Azure Container Apps

Justificación:
Permite desplegar y ejecutar el servicio responsable de las notificaciones.

---

# US-07: Reevaluación automática por tiempo de espera excedido

## S02

Actor:
- Enfermera

Impacto:
- Detectar pacientes que requieren reevaluación.

Deliverable:
- Sistema de alertas.

## S03

Contenedores relacionados:
- Backend API
- Motor de Clasificación IA
- Base de Datos

Justificación:
Permite generar alertas cuando un paciente supera los tiempos máximos de espera establecidos.

## S04

Servicios Cloud:
- Azure Machine Learning
- Azure Database for PostgreSQL

Justificación:
Permiten evaluar reglas clínicas y registrar alertas automáticamente.

---

# US-08: Autenticación de doble factor

## S02

Actor:
- Administrador

Impacto:
- Aumentar la seguridad de acceso al sistema.

Deliverable:
- Sistema de autenticación reforzada.

## S03

Contenedores relacionados:
- Frontend Web
- Backend API

Justificación:
Permite implementar autenticación de dos factores para proteger la información clínica.

## S04

Servicios Cloud:
- Azure Container Apps

Justificación:
Permite ejecutar el proceso de autenticación dentro del sistema.

---

# US-09: Registro y categorización de cancelaciones voluntarias

## S02

Actor:
- Enfermera

Impacto:
- Mantener actualizada la lista de pacientes en espera.

Deliverable:
- Registro de cancelaciones.

## S03

Contenedores relacionados:
- Frontend Web
- Backend API
- Base de Datos

Justificación:
Permite registrar y almacenar las cancelaciones realizadas por los pacientes.

## S04

Servicios Cloud:
- Azure Database for PostgreSQL

Justificación:
Permite mantener el historial de cancelaciones para análisis posteriores.

---

# US-10: Selección de idioma en el formulario del paciente

## S02

Actor:
- Paciente

Impacto:
- Mejorar la accesibilidad del sistema.

Deliverable:
- Formulario multilenguaje.

## S03

Contenedores relacionados:
- Frontend Web

Justificación:
Permite adaptar la interfaz a distintos idiomas.

## S04

Servicios Cloud:
- Azure Container Apps

Justificación:
Permite desplegar la interfaz web que ofrece soporte multilenguaje.

---

# Resumen de Evolución del Proyecto

S02
↓
Impact Map
↓
Historias de Usuario
↓
Backlog

↓

S03
↓
Arquitectura Monolito Modular
↓
C4 Nivel 1
↓
C4 Nivel 2

↓

S04
↓
Azure
↓
Servicios Gestionados
↓
Checklist 12-Factor
↓
ADR-0003
