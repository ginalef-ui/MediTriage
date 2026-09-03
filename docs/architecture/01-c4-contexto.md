# C4 - Nivel 1: Diagrama de Contexto del Sistema (MediTriage)

## 1. Propósito
El objetivo de este diagrama es ilustrar cómo interactúa **MediTriage** con los usuarios clínicos (enfermeros, médicos y administradores) y con los sistemas externos (modelos de IA local/nube y el sistema de información hospitalario), delimitando la frontera del sistema.

## 2. Diagrama C4 Contexto

```mermaid
C4Context
  title Diagrama de Contexto de Sistema (C4 Nivel 1) - MediTriage

  Person(enfermero, "Enfermero/a", "Ingresa datos y realiza la entrevista de triaje guiada.")
  Person(medico, "Médico/a", "Valida notas SOAP y participa en salas de discusión MDT.")
  Person(admin, "Administrador", "Gestiona accesos, roles y supervisa métricas del sistema.")

  System(meditriage, "MediTriage", "Sistema principal de triaje con IA y colaboración en tiempo real.")

  System_Ext(ollama, "Ollama Local (Llama 3.2)", "Servicio local para anonimizar y filtrar PII.")
  System_Ext(cloud_llm, "Cloud LLM API", "API de IA para análisis profundo y generación SOAP.")
  System_Ext(his, "HIS / Base de Datos", "Sistema de información hospitalaria y persistencia cifrada.")

  Rel(enfermero, meditriage, "Realiza triaje", "HTTPS")
  Rel(medico, meditriage, "Revisa SOAP y chat MDT", "HTTPS / WebSocket")
  Rel(admin, meditriage, "Gestiona el sistema", "HTTPS")

  Rel(meditriage, ollama, "Anonimiza datos sensibles", "REST / HTTP")
  Rel(meditriage, cloud_llm, "Solicita razonamiento de IA", "HTTPS / API")
  Rel(meditriage, his, "Guarda/Consulta registros médicos", "SQL / REST")
