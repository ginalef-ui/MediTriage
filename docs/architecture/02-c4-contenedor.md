# C4 - Nivel 2: Diagrama de Contenedores (MediTriage)

## 1. Propósito

El objetivo de este diagrama es mostrar la estructura interna del sistema **MediTriage**, descomponiendo el sistema principal en sus principales contenedores de software y almacenes de datos.

El diagrama permite identificar cómo interactúan las diferentes aplicaciones y módulos de MediTriage con los usuarios, la base de datos y los sistemas externos de inteligencia artificial e infraestructura hospitalaria.

---

## 2. Diagrama de Contenedores

```mermaid
flowchart TB

    %% =========================
    %% ESTILOS C4
    %% =========================

    classDef person fill:#08427b,stroke:#073b6f,color:#fff;
    classDef container fill:#1168bd,stroke:#0e5296,color:#fff;
    classDef database fill:#1168bd,stroke:#0e5296,color:#fff;
    classDef extSystem fill:#686868,stroke:#4a4a4a,color:#fff;


    %% =========================
    %% PERSONAS
    %% =========================

    PAC["<b>Paciente</b><br/><i>[Persona]</i><br/>Ingresa síntomas y consulta estado de espera."]:::person

    ENF["<b>Enfermero/a</b><br/><i>[Persona]</i><br/>Gestiona el triaje y reevaluación de pacientes."]:::person

    MED["<b>Médico/a</b><br/><i>[Persona]</i><br/>Consulta historial clínico y apoya la atención."]:::person

    AUD["<b>Auditor Clínico</b><br/><i>[Persona]</i><br/>Revisa y valida registros clínicos."]:::person

    ADM["<b>Administrador</b><br/><i>[Persona]</i><br/>Gestiona usuarios, roles y permisos."]:::person


    %% =========================
    %% CONTENEDORES MEDI TRIAGE
    %% =========================

    subgraph SISTEMA["MediTriage"]

        WEB["<b>Frontend Web / Móvil</b><br/><i>[Contenedor]</i><br/>Interfaz para pacientes y personal clínico.<br/><br/><b>Tecnología:</b> React / HTML / CSS / JavaScript"]:::container

        API["<b>Backend / API</b><br/><i>[Contenedor]</i><br/>Gestiona las solicitudes y coordina los módulos del sistema.<br/><br/><b>Tecnología:</b> Node.js + Express"]:::container

        TRIAGE["<b>Módulo de Triaje</b><br/><i>[Contenedor]</i><br/>Procesa síntomas y genera la clasificación asistida.<br/><br/><b>Tecnología:</b> Node.js"]:::container

        CLINICO["<b>Módulo Clínico</b><br/><i>[Contenedor]</i><br/>Gestiona historial, síntomas y clasificación previa.<br/><br/><b>Tecnología:</b> Node.js"]:::container

        AUDITORIA["<b>Módulo de Auditoría</b><br/><i>[Contenedor]</i><br/>Permite revisar y validar registros clínicos.<br/><br/><b>Tecnología:</b> Node.js"]:::container

        ADMIN["<b>Módulo de Administración</b><br/><i>[Contenedor]</i><br/>Gestiona usuarios, roles y permisos.<br/><br/><b>Tecnología:</b> Node.js"]:::container

        NOTIFICACIONES["<b>Servicio de Notificaciones</b><br/><i>[Contenedor]</i><br/>Envía alertas y actualizaciones del estado de espera.<br/><br/><b>Tecnología:</b> WebSocket"]:::container

        DB[("<b>Base de Datos MediTriage</b><br/><i>[Contenedor - Almacén de datos]</i><br/>Pacientes, síntomas, clasificaciones,<br/>usuarios, auditorías y registros.<br/><br/><b>Tecnología:</b> PostgreSQL")]:::database

    end


    %% =========================
    %% SISTEMAS EXTERNOS
    %% =========================

    OLL["<b>Ollama Local</b><br/><i>[Sistema Externo]</i><br/>Anonimización de información sensible."]:::extSystem

    LLM["<b>Cloud LLM API</b><br/><i>[Sistema Externo]</i><br/>Razonamiento clínico y generación de notas SOAP."]:::extSystem

    HIS["<b>HIS / BD Hospital</b><br/><i>[Sistema Externo]</i><br/>Persistencia e información clínica hospitalaria."]:::extSystem


    %% =========================
    %% INTERACCIONES USUARIOS
    %% =========================

    PAC -->|"Ingresa síntomas y datos<br/>[HTTPS]"| WEB

    ENF -->|"Gestiona triaje y reevaluación<br/>[HTTPS]"| WEB

    MED -->|"Consulta historial clínico<br/>[HTTPS]"| WEB

    AUD -->|"Revisa registros clínicos<br/>[HTTPS]"| WEB

    ADM -->|"Gestiona usuarios, roles y permisos<br/>[HTTPS]"| WEB


    %% =========================
    %% FRONTEND → BACKEND
    %% =========================

    WEB -->|"Solicitudes de aplicación<br/>[HTTPS / REST]"| API


    %% =========================
    %% BACKEND → MÓDULOS
    %% =========================

    API -->|"Gestiona clasificación"| TRIAGE

    API -->|"Gestiona información clínica"| CLINICO

    API -->|"Gestiona auditorías"| AUDITORIA

    API -->|"Gestiona usuarios y permisos"| ADMIN

    API -->|"Envía alertas y actualizaciones"| NOTIFICACIONES


    %% =========================
    %% MÓDULOS → BASE DE DATOS
    %% =========================

    TRIAGE -->|"Lee y registra síntomas<br/>y clasificación [SQL]"| DB

    CLINICO -->|"Consulta y actualiza historial<br/>[SQL]"| DB

    AUDITORIA -->|"Consulta registros y auditorías<br/>[SQL]"| DB

    ADMIN -->|"Gestiona usuarios, roles<br/>y permisos [SQL]"| DB

    NOTIFICACIONES -->|"Consulta estado de espera<br/>[SQL]"| DB


    %% =========================
    %% IA
    %% =========================

    TRIAGE -->|"Anonimiza información sensible<br/>[REST / HTTP]"| OLL

    TRIAGE -->|"Solicita análisis clínico<br/>[HTTPS / API]"| LLM


    %% =========================
    %% INTEGRACIÓN HOSPITALARIA
    %% =========================

    CLINICO -->|"Consulta información clínica<br/>[SQL / REST]"| HIS
