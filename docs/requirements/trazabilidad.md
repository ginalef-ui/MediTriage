# Trazabilidad S03 → S04
# Proyecto: MediTriage

Esta sección relaciona la arquitectura definida en la S03 con las decisiones cloud tomadas en la S04.

---

## Frontend Web

### S03

Tecnología:
- React

Función:
- Interfaz para pacientes, enfermeras, médicos y administradores.

### S04

Servicios Cloud Asociados:
- Azure Container Apps

Justificación:
Permite desplegar la aplicación Frontend sin administrar infraestructura propia.

---

## Backend API

### S03

Tecnología:
- Node.js + Express

Función:
- Implementar la lógica de negocio del sistema MediTriage.

### S04

Servicios Cloud Asociados:
- Azure Container Apps

Justificación:
Permite desplegar el Backend y escalar automáticamente según la demanda.

---

## Base de Datos Clínica

### S03

Tecnología:
- PostgreSQL

Función:
- Almacenar pacientes, síntomas, historiales clínicos y usuarios.

### S04

Servicios Cloud Asociados:
- Azure Database for PostgreSQL

Justificación:
Proporciona persistencia de datos, respaldos automáticos y alta disponibilidad.

---

## Módulo de Auditoría

### S03

Función:
- Registrar acciones críticas y decisiones clínicas.

### S04

Servicios Cloud Asociados:
- Azure SQL Database Ledger

Justificación:
Permite mantener registros verificables e inmutables para auditoría.

---

## Motor de Clasificación IA

### S03

Tecnología:
- Python

Función:
- Clasificar pacientes según síntomas y criterios de urgencia.

### S04

Servicios Cloud Asociados:
- Azure Machine Learning

Justificación:
Permite entrenar, desplegar y administrar modelos de IA en un entorno gestionado.

---

## Gestión de Calidad y Despliegue

### S03

Función:
- Integración continua y validación del sistema.

### S04

Servicios Cloud Asociados:
- GitHub Actions

Justificación:
Automatiza pruebas, validaciones y despliegues del proyecto.

---

# Resumen de Evolución

S02
↓
Impact Map

↓

Historias de Usuario

↓
S03

Arquitectura Monolito Modular

C4 Nivel 1

C4 Nivel 2

↓
S04

Azure

Servicios Gestionados

12-Factor

ADR-0003
``
