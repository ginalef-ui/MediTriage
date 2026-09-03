# C4 - Nivel 1: Diagrama de Contexto del Sistema (MediTriage)
2
 
3
## 1. Propósito
4
 
5
El objetivo de este diagrama es ilustrar el límite del sistema **MediTriage**, mostrando cómo interactúan los usuarios clínicos con él y cómo se integra con sistemas externos de soporte de IA e infraestructura hospitalaria.
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
flowchart LR
13
 
14
ENF["Enfermero/a"]
15
MED["Médico/a"]
16
ADM["Administrador"]
17
 
18
SYS["MediTriage
19
Sistema de triaje asistido por IA"]
20
 
21
OLL["Ollama Local
22
Anonimización PII"]
23
 
24
LLM["Cloud LLM API
25
Generación de notas SOAP"]
26
 
27
HIS["HIS / Base de Datos Hospital"]
28
 
29
ENF -->|"Realiza entrevista de triaje"| SYS
30
MED -->|"Revisa notas SOAP y participa en MDT"| SYS
31
ADM -->|"Administra usuarios y métricas"| SYS
32
 
33
SYS -->|"Anonimiza datos"| OLL
34
SYS -->|"Solicita análisis clínico"| LLM
35
SYS -->|"Guarda y consulta registros"| HIS
36
```
37
 
38
---
39
 
40
## 3. Descripción de Elementos
41
 
42
### 3.1 Usuarios
43
 
44
| Actor | Descripción | Responsabilidad Principal |
45
|---------|-------------|-------------------------|
46
| Enfermero/a | Personal clínico de primera línea. | Captura constantes vitales, síntomas y ejecuta el proceso de triaje. |
47
| Médico/a | Profesional médico tratante o especialista. | Valida y corrige las notas SOAP generadas por IA y participa en la colaboración clínica. |
48
| Administrador | Personal de TI u operaciones hospitalarias. | Gestiona accesos, roles, auditorías y métricas del sistema. |
49
 
50
### 3.2 Sistemas
51
 
52
| Sistema | Tipo | Descripción |
53
|----------|------|-------------|
54
| MediTriage | Sistema Central | Plataforma web/móvil que gestiona el flujo de triaje asistido por IA y colaboración médica. |
55
| Ollama Local | Sistema Externo | Servicio local encargado de anonimizar la información sensible del paciente antes de enviarla a servicios externos. |
56
| Cloud LLM API | Sistema Externo | Servicio de inteligencia artificial utilizado para el razonamiento clínico y la generación de notas SOAP. |
57
| HIS / Base de Datos Hospital | Sistema Externo | Sistema de información hospitalaria responsable del almacenamiento permanente de los registros clínicos. |
58
 
59
---
60
 
61
## 4. Alcance del Sistema
62
 
63
### Dentro del alcance de MediTriage
64
 
65
- Captura asistida de datos de triaje.
66
- Anonimización local de información sensible.
67
- Generación y edición de notas SOAP.
68
- Comunicación en tiempo real mediante salas MDT.
69
- Gestión de usuarios y permisos.
70
 
71
### Fuera del alcance
72
 
73
- Administración histórica de fichas clínicas a largo plazo (HIS).
74
- Entrenamiento de modelos de inteligencia artificial.
75
- Autenticación corporativa externa (Active Directory, OAuth u otros servicios institucionales).
76
 
77
---
78
 
79
## 5. Decisiones de Arquitectura
80
 
81
### Privacidad y Cumplimiento
82
 
83
Se adopta una arquitectura híbrida de inteligencia artificial. Los datos identificables del paciente son anonimizados localmente antes de enviarse a servicios de IA en la nube.
84
 
85
### Comunicación en Tiempo Real
86
 
87
La colaboración entre profesionales clínicos se realiza mediante mecanismos de comunicación en tiempo real para facilitar la toma de decisiones durante emergencias y reuniones multidisciplinarias.
88
 
89
### Integración Hospitalaria
90
 
91
La persistencia de la información clínica se delega al sistema HIS institucional, evitando duplicidad de registros y manteniendo la integración con la infraestructura existente.
