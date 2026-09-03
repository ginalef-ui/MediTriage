# C4 - Nivel 1: Diagrama de Contexto del Sistema (MediTriage)

## 1. Propósito
El objetivo de este diagrama es ilustrar las interacciones entre los usuarios clínicos (**Enfermeros, Médicos y Administradores**) y el sistema **MediTriage**, así como sus conexiones con los sistemas externos (**IA Local, IA en Nube y Sistema Hospitalario HIS**).

---

## 2. Diagrama de Contexto

```mermaid
flowchart TB
    classDef person fill:#08427b,stroke:#073b6f,color:#fff,rx:10,ry:10;
    classDef system fill:#1168bd,stroke:#0e5296,color:#fff,rx:5,ry:5;
    classDef extSystem fill:#686868,stroke:#4a4a4a,color:#fff,rx:5,ry:5;

    subgraph Actores [" Usuarios del Sistema "]
        ENF["<b>Enfermero/a</b><br/><i>[Persona]</i><br/>Ingresa datos y realiza la<br/>entrevista de triaje guiada."]:::person
        MED["<b>Médico/a</b><br/><i>[Persona]</i><br/>Valida notas SOAP y participa<br/>en salas de discusión MDT."]:::person
        ADM["<b>Administrador</b><br/><i>[Persona]</i><br/>Gestiona accesos, roles y<br/>supervisa métricas del sistema."]:::person
    end

    SYS["<b>MediTriage</b><br/><i>[Sistema Principal]</i><br/>Sistema de triaje asistido por IA y<br/>colaboración médica en tiempo real."]:::system

    subgraph Externos [" Sistemas Externos "]
        OLL["<b>Ollama Local (Llama 3.2)</b><br/><i>[Sistema Externo]</i><br/>Servicio local para anonimizar<br/>y filtrar PII."]:::extSystem
        LLM["<b>Cloud LLM API</b><br/><i>[Sistema Externo]</i><br/>API de IA para análisis profundo<br/>y generación de notas SOAP."]:::extSystem
        HIS["<b>HIS / BD Hospital</b><br/><i>[Sistema Externo]</i><br/>Sistema de información hospitalaria<br/>y persistencia cifrada."]:::extSystem
    end

    ENF -->|"Realiza entrevista de triaje<br/>[HTTPS]"| SYS
    MED -->|"Revisa SOAP / Chat MDT<br/>[HTTPS / WebSocket]"| SYS
    ADM -->|"Administra el sistema<br/>[HTTPS]"| SYS

    SYS -->|"1. Anonimiza PII<br/>[REST / HTTP]"| OLL
    SYS -->|"2. Solicita razonamiento IA<br/>[HTTPS / API]"| LLM
    SYS -->|"3. Guarda/Consulta registros<br/>[SQL / REST]"| HIS
## 3. Descripción de Elementos

### Usuarios (Personas)
| Elemento | Tipo | Descripción |
| :--- | :--- | :--- |
| **Enfermero/a** | Persona | Registra los síntomas iniciales del paciente y realiza la entrevista asistida por la IA durante el triaje. |
| **Médico/a** | Persona | Revisa los borradores de notas SOAP generados automáticamente, realiza diagnósticos finales y participa en el chat MDT en tiempo real. |
| **Administrador** | Persona | Gestiona la creación de usuarios, asignación de roles (RBAC) y audita el uso del sistema. |

### Sistema Principal
| Elemento | Tipo | Descripción |
| :--- | :--- | :--- |
| **MediTriage** | Sistema | Plataforma web central encargada de orquestar el triaje, la anonimización de datos, la comunicación con los LLMs y la colaboración clínica. |

### Sistemas Externos
| Elemento | Tipo | Descripción |
| :--- | :--- | :--- |
| **Ollama Local (Llama 3.2)** | Sistema Externo | Modelo ejecutable en la red local del hospital encargada del *scrubbing* (eliminación) de PII para proteger la privacidad del paciente. |
| **Cloud LLM API** | Sistema Externo | Modelos avanzados en la nube (ej. DeepSeek, OpenAI) encargados de la generación de razonamiento clínico sobre datos anonimizados. |
| **HIS / Base de Datos** | Sistema Externo | Sistema de Información Hospitalaria y base de datos para la persistencia del historial clínico cifrado (AES-256). |
