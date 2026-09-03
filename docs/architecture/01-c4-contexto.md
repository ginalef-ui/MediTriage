# C4 - Nivel 1: Diagrama de Contexto del Sistema (MediTriage)

## 1. Propósito

El objetivo de este diagrama es ilustrar el límite del sistema **MediTriage**, mostrando cómo interactúan los usuarios clínicos con él y cómo se integra con sistemas externos de soporte de IA e infraestructura hospitalaria.

---

## 2. Diagrama de Contexto

```mermaid
flowchart TB
    classDef person fill:#08427b,stroke:#073b6f,color:#fff;
    classDef system fill:#1168bd,stroke:#0e5296,color:#fff;
    classDef extSystem fill:#686868,stroke:#4a4a4a,color:#fff;

    subgraph Actores ["Usuarios del Sistema"]
        ENF["<b>Enfermero/a</b><br/><i>[Persona]</i><br/>Captura datos y ejecuta triaje."]:::person
        MED["<b>Médico/a</b><br/><i>[Persona]</i><br/>Valida notas SOAP y colabora en MDT."]:::person
        ADM["<b>Administrador</b><br/><i>[Persona]</i><br/>Gestiona usuarios, roles y métricas."]:::person
    end

    SYS["<b>MediTriage</b><br/><i>[Sistema Principal]</i><br/>Sistema de triaje asistido por IA."]:::system

    subgraph Externos ["Sistemas Externos"]
        OLL["<b>Ollama Local</b><br/><i>[Sistema Externo]</i><br/>Anonimización de PII."]:::extSystem
        LLM["<b>Cloud LLM API</b><br/><i>[Sistema Externo]</i><br/>Razonamiento y notas SOAP."]:::extSystem
        HIS["<b>HIS / BD Hospital</b><br/><i>[Sistema Externo]</i><br/>Persistencia e información clínica."]:::extSystem
    end

    ENF -->|"Realiza entrevista de triaje<br/>[HTTPS]"| SYS
    MED -->|"Revisa SOAP / Chat MDT<br/>[HTTPS / WebSocket]"| SYS
    ADM -->|"Administra usuarios y métricas<br/>[HTTPS]"| SYS

    SYS -->|"1. Anonimiza datos<br/>[REST / HTTP]"| OLL
    SYS -->|"2. Solicita análisis clínico<br/>[HTTPS / API]"| LLM
    SYS -->|"3. Guarda y consulta registros<br/>[SQL / REST]"| HIS
