# Política de Versionado y Compatibilidad de la API - MediTriage

## 1. Estrategia de Versionado
MediTriage utiliza **versionado explícito en la URL** (URI Versioning).
El prefijo de la versión mayor se incluirá en la ruta base de todos los endpoints.
Ejemplo de ruta: `https://api.meditriage.cl/v1/triage`

## 2. Reglas de Compatibilidad (Backwards Compatibility)
Nuestra regla estricta de diseño es **nunca romper contratos existentes**. 

Las siguientes modificaciones están **permitidas** en la versión actual (`v1`) porque no rompen la compatibilidad:
- Agregar nuevos endpoints al sistema.
- Agregar nuevos campos opcionales en los cuerpos de petición (request).
- Agregar nuevos campos en las respuestas (response).
- Agregar nuevos encabezados HTTP opcionales.

Las siguientes modificaciones **rompen la compatibilidad** y forzarán la creación de una nueva versión de la API (ej. pasar a `v2`):
- Eliminar o renombrar campos, parámetros o endpoints existentes.
- Cambiar el tipo de dato de un campo (ej. de `string` a `integer`).
- Convertir un campo que antes era opcional en obligatorio.

## 3. Política de Deprecación
Si un endpoint específico o una versión completa de la API necesita ser retirada:
- Se notificará a los consumidores y clientes (partners, frontend móvil) con un periodo mínimo de transición.
- Se incluirá la cabecera estándar HTTP `Deprecation: true` en las respuestas de los endpoints afectados.
- La documentación viva del contrato OpenAPI (Swagger UI / Redoc) marcará visualmente los endpoints con el tag `[DEPRECATED]`.
