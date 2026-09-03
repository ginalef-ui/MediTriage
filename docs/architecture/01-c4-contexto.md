# C4 - Nivel 1: Diagrama de Contexto del Sistema (MediTriage)
2
 
3
## 1. Propósito
4
 
5
El objetivo de este diagrama es ilustrar el límite del sistema **MediTriage**, mostrando cómo interactúan los usuarios clínicos con él y cómo se integra con los sistemas externos de soporte de IA e infraestructura hospitalaria.
6
 
7
---
8
 
9
## 2. Diagrama de Contexto
10
 
11
```mermaid
12
flowchart TB
13
 
14
classDef person fill:#08427b,stroke:#073b6f,color:#fff;
15
classDef system fill:#1168bd,stroke:#0e5296,color:#fff;
16
classDef extSystem fill:#686868,stroke:#4a4a4a,color:#fff;
17
 
18
subgraph Actores["Usuarios del Sistema"]
19
ENF["<b>Enfermero/a</b><br/><i>[Persona]</i><br/>Ingresa datos y realiza la<br/>entrevista de triaje guiada."]:::person
20
MED["<b>Médico/a</b><br/><i>[Persona]</i><br/>Valida notas SOAP y participa<br/>en salas de discusión MDT."]:::person
21
ADM["<b>Administrador</b><br/><i>[Persona]</i><br/>Gestiona accesos, roles y<br/>supervisa métricas del sistema."]:::person
22
end
23
 
24
SYS["<b>MediTriage</b><br/><i>[Sistema Principal]</i><br/>Sistema de triaje asistido por IA y<br/>colaboración médica en tiempo real."]:::system
25
 
26
subgraph Externos["Sistemas Externos"]
27
OLL["<b>Ollama Local (Llama 3.2)</b><br/><i>[Sistema Externo]</i><br/>Servicio local para anonimizar<br/>y filtrar PII."]:::extSystem
28
LLM["<b>Cloud LLM API</b><br/><i>[Sistema Externo]</i><br/>API de IA para análisis profundo<br/>y generación de notas SOAP."]:::extSystem
29
HIS["<b>HIS / BD Hospital</b><br/><i>[Sistema Externo]</i><br/>Sistema de información hospitalaria<br/>y persistencia cifrada."]:::extSystem
30
end
31
 
32
ENF -->|"Realiza entrevista de triaje<br/>[HTTPS]"| SYS
33
MED -->|"Revisa SOAP / Chat MDT<br/>[HTTPS / WebSocket]"| SYS
34
ADM -->|"Administra el sistema<br/>[HTTPS]"| SYS
35
 
36
SYS -->|"1. Anonimiza PII<br/>[REST / HTTP]"| OLL
37
SYS -->|"2. Solicita razonamiento IA<br/>[HTTPS / API]"| LLM
38
SYS -->|"3. Guarda/Consulta registros<br/>[SQL / REST]"| HIS
39
```
40
 
41
---
42
 
43
## 3. Descripción de Elementos
44
 
45
### 3.1. Usuarios (Personas)
46
 
47
| Actor | Descripción | Responsabilidad Principal |
48
|---------|-------------|-------------------------|
49
| **Enfermero/a** | Personal clínico en primera línea de atención. | Captura de constantes vitales, sintomatología y ejecución del triaje. |
50
| **Médico/a** | Profesional médico tratante o especialista. | Validación o edición de la nota SOAP generada por IA y colaboración en tiempo real. |
51
| **Administrador** | Personal de TI u operaciones hospitalarias. | Gestión de usuarios, asignación de roles y monitoreo de auditoría. |
52
 
53
### 3.2. Sistemas
54
 
55
| Sistema | Tipo | Descripción / Tecnología |
56
|----------|------|--------------------------|
57
| **MediTriage** | Sistema Central | Plataforma web/móvil que orquesta el flujo de triaje, anonimización, inferencia de IA y comunicación en tiempo real. |
58
| **Ollama Local** | Sistema Externo | Instancia local (ej. Llama 3.2) encargada de detectar y remover Datos de Identificación Personal (PII) antes de cualquier envío a la nube. |
59
| **Cloud LLM API** | Sistema Externo | Modelo de lenguaje de alta capacidad utilizado para razonamiento clínico estructurado y redacción de notas SOAP. |
60
| **HIS / BD Hospital** | Sistema Externo | Sistema de Información Hospitalaria (registro clínico electrónico) donde se persisten los datos del paciente y fichas clínicas. |
61
 
62
---
63
 
64
## 4. Límites del Alcance (In Scope / Out of Scope)
65
 
66
### Dentro del alcance (MediTriage)
67
 
68
- Interfaz de captura de triaje asistida.
69
- Pipeline de sanitización de datos (anonimización local).
70
- Generación y edición colaborativa de notas SOAP.
71
- Chat y salas MDT en tiempo real mediante WebSockets.
72
 
73
### Fuera del alcance (Sistemas Externos)
74
 
75
- Gestión centralizada de fichas del paciente a largo plazo (delegado al **HIS**).
76
- Entrenamiento o fine-tuning de los modelos de IA (delegado a los proveedores de **LLM**).
77
- Autenticación corporativa centralizada (si se integra con Active Directory u OAuth del hospital).
78
 
79
---
80
 
81
## 5. Decisiones Clave de Arquitectura (Nivel Contexto)
82
 
83
1. **Privacidad y Cumplimiento (HIPAA/GDPR):**
84
Se optó por una arquitectura híbrida de IA. Ningún dato identificable del paciente sale de la red local del hospital hacia servicios cloud.
85
 
86
2. **Comunicación Bidireccional:**
87
El uso de WebSockets es indispensable para la colaboración médica sincrónica durante emergencias o discusiones multidisciplinarias.
