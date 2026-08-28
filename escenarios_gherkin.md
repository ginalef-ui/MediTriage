# Escenarios Gherkin - MediTriage

---

# US-01: Registro de síntomas del paciente

## Escenario 1: Registro exitoso de síntomas

**Given** - El paciente se encuentra en el formulario digital de registro  
**When** - Completa todos los campos obligatorios con información válida  
**And** - Envía el formulario  
**Then** - El sistema registra correctamente los síntomas y datos del paciente

## Escenario 2: Registro con información opcional incompleta

**Given** - El paciente se encuentra en el formulario digital de registro  
**When** - Completa todos los campos obligatorios  
**And** - Deja vacíos algunos campos opcionales  
**Then** - El sistema permite registrar la información del paciente correctamente

## Escenario 3: Registro con campos obligatorios vacíos

**Given** - El paciente se encuentra en el formulario digital de registro  
**When** - Intenta enviar el formulario sin completar todos los campos obligatorios  
**Then** - El sistema informa cuáles son los campos que deben ser completados para realizar el registro

---

# US-02: Visualización de prioridad de pacientes

## Escenario 1: Visualización correcta de la clasificación

**Given** - La enfermera ha iniciado sesión en el sistema  
**And** - Existen pacientes registrados con diferentes niveles de urgencia  
**When** - Accede al sistema de clasificación asistida  
**Then** - El sistema muestra a los pacientes según su nivel de prioridad

## Escenario 2: Consulta sin pacientes pendientes

**Given** - La enfermera ha iniciado sesión en el sistema  
**And** - No existen pacientes pendientes de atención  
**When** - Accede al sistema de clasificación asistida  
**Then** - El sistema informa que no existen pacientes pendientes

## Escenario 3: Acceso sin permisos a la clasificación

**Given** - Un usuario no cuenta con permisos de enfermera  
**When** - Intenta acceder al sistema de clasificación asistida  
**Then** - El sistema deniega el acceso al módulo

---

# US-03: Consulta de historial clínico

## Escenario 1: Visualización exitosa del historial clínico

**Given** - El médico ha iniciado sesión en el sistema  
**And** - El paciente posee información clínica registrada  
**When** - El médico consulta el historial del paciente  
**Then** - El sistema muestra los síntomas y la clasificación previa del paciente

## Escenario 2: Paciente sin historial clínico previo

**Given** - El médico ha iniciado sesión en el sistema  
**And** - El paciente no posee registros clínicos anteriores  
**When** - El médico consulta el historial del paciente  
**Then** - El sistema informa que no existen registros clínicos previos

## Escenario 3: Consulta de paciente no registrado

**Given** - El médico ha iniciado sesión en el sistema  
**When** - Busca un paciente que no se encuentra registrado  
**Then** - El sistema informa que el paciente no fue encontrado

---

# US-04: Auditoría y revisión de registros clínicos

## Escenario 1: Revisión exitosa de un registro clínico

**Given** - El auditor clínico ha iniciado sesión en el sistema  
**And** - Existen registros clínicos disponibles para revisión  
**When** - Selecciona un registro clínico  
**Then** - El sistema muestra la información necesaria para revisar el proceso de clasificación

## Escenario 2: Consulta sin registros disponibles

**Given** - El auditor clínico ha iniciado sesión en el sistema  
**And** - No existen registros clínicos disponibles para auditoría  
**When** - Accede al módulo de auditoría  
**Then** - El sistema informa que no existen registros disponibles para revisar

## Escenario 3: Acceso no autorizado al módulo de auditoría

**Given** - Un usuario no cuenta con permisos de auditor clínico  
**When** - Intenta acceder al módulo de auditoría  
**Then** - El sistema deniega el acceso al módulo

---

# US-05: Panel de administración y permisos

## Escenario 1: Gestión exitosa de un usuario

**Given** - El administrador ha iniciado sesión en el sistema  
**When** - Crea un nuevo usuario y le asigna un rol válido  
**Then** - El sistema registra al usuario con los permisos correspondientes

## Escenario 2: Modificación de permisos de un usuario

**Given** - El administrador ha iniciado sesión en el sistema  
**And** - Existe un usuario registrado  
**When** - Modifica el rol o los permisos del usuario  
**Then** - El sistema actualiza correctamente los permisos asignados

## Escenario 3: Creación de usuario con información incompleta

**Given** - El administrador ha iniciado sesión en el sistema  
**When** - Intenta crear un usuario sin completar los datos obligatorios  
**Then** - El sistema informa que debe completar la información requerida para proceder con la acciÓn
