# Servicios Gestionados (Azure)
Para soportar la arquitectura de Monolito Modular y cubrir los requerimientos técnicos del proyecto, se seleccionaron los siguientes 5 servicios gestionados en la nube de Azure:

## 1. Azure Container Apps (Infraestructura / DevOps):
Servicio serverless que permite a Vicente desplegar el código empaquetado en contenedores. Elimina la necesidad de administrar servidores subyacentes y garantiza que el sistema escale automáticamente si hay un alto flujo de pacientes.

## 2. Azure Database for PostgreSQL (Base de Datos / Tech Lead):
Base de datos relacional gestionada. Seleccionada por Genessis para asegurar la persistencia, escalabilidad y respaldos automáticos de los formularios digitales y los historiales clínicos.

## 3. Azure SQL Database Ledger (Auditoría / SecOps):
Proporciona un registro de transacciones inmutable y verificable criptográficamente. Cubre la necesidad crítica de Elias de mantener un historial inalterable de las priorizaciones generadas por el sistema.

## 4. Azure Machine Learning (IA / AI Lead):
Entorno completamente gestionado que permite a José alojar el motor de clasificación asistida, asegurando que el modelo evalúe los síntomas rápidamente para el tablero de enfermería.

## 5. GitHub Actions (CI/CD y Calidad / QA Lead):
Herramienta de integración y despliegue continuo nativa. Permite automatizar la revisión de código y las pruebas de Marcela para cumplir con la Definition of Done (DoD) antes de enviar cualquier actualización a producción.
