
# 12 FACTORES

## 1. Codebase
**NO CUMPLE**

**Propuesta**: Consolidar el monolito modular en un único repositorio Git en GitHub y configurar políticas de protección de ramas.

**Rol a cargo**: SecOps (Elias Galdames)

## 2. Dependencies
**NO CUMPLE**

**Propuesta**: Aislar las dependencias en Docker y declararlas explícitamente en el package.json para evitar el uso de paquetes globales.

**Rol a cargo**: Tech lead (Genessis Inalef)

## 3. Config
**NO CUMPLE**

**Propuesta**: Extraer las credenciales (PostgreSQL, APIs de LLM) del código fuente y migrarlas a Secrets en Azure y variables .env.

**Rol a cargo**: SecOps (Elias Galdames)

## 4. Backing services
**NO CUMPLE**

**Propuesta**: Tratar Azure PostgreSQL y Azure SQL Ledger como recursos externos acoplables mediante cadenas de conexión por URL.

**Rol a cargo**: Tech lead (Genessis Inalef)

## 5. Build, release, run
**NO CUMPLE**

**Propuesta**: Automatizar el flujo en GitHub Actions para separar estrictamente la fase de compilación del despliegue en Azure Container Apps.

**Rol a cargo**: DevOps (Vicente Cosio)

## 6. Processes
**SI CUMPLE**

**Propuesta**: El backend en Node.js delega todo el almacenamiento de estado clínico y sesiones directamente a la base de datos PostgreSQL.

**Rol a cargo**: Sin Asignar

## 7. Port binding
**NO CUMPLE**

**Propuesta**: Ajustar el servidor Express para que escuche dinámicamente el puerto asignado por Azure mediante process.env.PORT.

**Rol a cargo**: Tech lead (Genessis Inalef)

## 8. Concurrency
**NO CUMPLE**

**Propuesta**: Configurar las reglas de escalado horizontal en Azure Container Apps para levantar múltiples réplicas ante alta demanda en urgencias.

**Rol a cargo**: DevOps (Vicente Cosio)

## 9. Dsiposability
**NO CUMPLE**

**Propuesta**: Implementar graceful shutdown en Node.js capturando señales SIGTERM para cerrar los WebSockets y conexiones SQL de forma segura.

**Rol a cargo**: Tech lead (Genessis Inalef)

## 10. Dev / Prod parity
**NO CUMPLE**

**Propuesta**: Crear un archivo docker-compose.yml para que el entorno local replique la misma versión de PostgreSQL y Node.js usada en Azure.

**Rol a cargo**: QA (Marcela Manzor)

## 11. Logs
**NO CUMPLE**

**Propuesta**: Enviar los eventos de auditoría y errores directamente a la salida estándar (stdout/stderr) para que sean centralizados por Azure Monitor.

**Rol a cargo**: SecOps (Elias Galdames)

## 12. Admin processes
**NO CUMPLE**

**Propuesta**: Configurar la ejecución de tareas administrativas (como las migraciones de esquemas en PostgreSQL) en el mismo entorno de ejecución.

**Rol a cargo**: DevOps (Vicente Cosio)
