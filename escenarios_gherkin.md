# Escenarios Gherkin - MediTriage

---

# US-01: Registro de síntomas del paciente

## Escenario 1: Registro exitoso de síntomas

Given el paciente se encuentra en el formulario digital de registro
When completa todos los campos obligatorios con información válida
And envía el formulario
Then el sistema registra correctamente los síntomas y datos del paciente

## Escenario 2: Registro con información opcional incompleta

Given el paciente se encuentra en el formulario digital de registro
When completa todos los campos obligatorios
And deja vacíos algunos campos opcionales
Then el sistema permite registrar la información del paciente correctamente

## Escenario 3: Registro con campos obligatorios vacíos

Given el paciente se encuentra en el formulario digital de registro
When intenta enviar el formulario sin completar todos los campos obligatorios
Then el sistema informa cuáles son los campos que deben ser completados

---

# US-02: Visualización de prioridad de pacientes

## Escenario 1: Visualización correcta de la clasificación

Given la enfermera ha iniciado sesión en el sistema
And existen pacientes registrados con diferentes niveles de urgencia
When accede al sistema de clasificación asistida
Then el sistema muestra a los pacientes según su nivel de prioridad

## Escenario 2: Consulta sin pacientes pendientes

Given la enfermera ha iniciado sesión en el sistema
And no existen pacientes pendientes de atención
When accede al sistema de clasificación asistida
Then el sistema informa que no existen pacientes pendientes

## Escenario 3: Acceso sin permisos a la clasificación

Given un usuario no cuenta con permisos de enfermera
When intenta acceder al sistema de clasificación asistida
Then el sistema deniega el acceso al módulo

---

# US-03: Consulta de historial clínico

## Escenario 1: Visualización exitosa del historial clínico

Given el médico ha iniciado sesión en el sistema
And el paciente posee información clínica registrada
When el médico consulta el historial del paciente
Then el sistema muestra los síntomas y la clasificación previa del paciente

## Escenario 2: Paciente sin historial clínico previo

Given el médico ha iniciado sesión en el sistema
And el paciente no posee registros clínicos anteriores
When el médico consulta el historial del paciente
Then el sistema informa que no existen registros clínicos previos

## Escenario 3: Consulta de paciente no registrado

Given el médico ha iniciado sesión en el sistema
When busca un paciente que no se encuentra registrado
Then el sistema informa que el paciente no fue encontrado

---

# US-04: Auditoría y revisión de registros clínicos

## Escenario 1: Revisión exitosa de un registro clínico

Given el auditor clínico ha iniciado sesión en el sistema
And existen registros clínicos disponibles para revisión
When selecciona un registro clínico
Then el sistema muestra la información necesaria para revisar el proceso de clasificación

## Escenario 2: Consulta sin registros disponibles

Given el auditor clínico ha iniciado sesión en el sistema
And no existen registros clínicos disponibles para auditoría
When accede al módulo de auditoría
Then el sistema informa que no existen registros disponibles para revisar

## Escenario 3: Acceso no autorizado al módulo de auditoría

Given un usuario no cuenta con permisos de auditor clínico
When intenta acceder al módulo de auditoría
Then el sistema deniega el acceso al módulo

---

# US-05: Panel de administración y permisos

## Escenario 1: Gestión exitosa de un usuario

Given el administrador ha iniciado sesión en el sistema
When crea un nuevo usuario y le asigna un rol válido
Then el sistema registra al usuario con los permisos correspondientes

## Escenario 2: Modificación de permisos de un usuario

Given el administrador ha iniciado sesión en el sistema
And existe un usuario registrado
When modifica el rol o los permisos del usuario
Then el sistema actualiza correctamente los permisos asignados

## Escenario 3: Creación de usuario con información incompleta

Given el administrador ha iniciado sesión en el sistema
When intenta crear un usuario sin completar los datos obligatorios
Then el sistema informa que debe completar la información requerida
