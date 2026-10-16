# ADR-0005: Plataforma Kubernetes e Infraestructura como Código

## Estado

Aceptado

## Contexto

MediTriage necesita contar con un entorno que permita probar y validar el despliegue de sus servicios utilizando contenedores y Kubernetes. Para facilitar estas pruebas, es necesario seleccionar una distribución de Kubernetes que pueda ejecutarse localmente, una herramienta para definir la infraestructura mediante código y una imagen base para construir el contenedor del backend.

La solución debe permitir realizar pruebas reproducibles, mantener una configuración organizada y facilitar futuras modificaciones de la infraestructura.

## Decisiones

### 1. Plataforma Kubernetes para pruebas

Se utilizará **K3d** para crear y ejecutar clústeres locales de Kubernetes durante las pruebas y el desarrollo del proyecto.

K3d permite ejecutar K3s dentro de contenedores Docker, facilitando la creación y eliminación de entornos locales sin necesitar inicialmente un clúster Kubernetes en la nube.

Se selecciona esta alternativa para simplificar las pruebas del despliegue de MediTriage y facilitar la reproducción del entorno entre los integrantes del equipo.

### 2. Herramienta de Infraestructura como Código

Se utilizará **Terraform** para definir y administrar la infraestructura mediante archivos de configuración.

Esta herramienta permite describir los recursos de manera declarativa, mantener la configuración versionada en Git y facilitar la reproducción de los entornos.

La configuración incluirá los recursos necesarios para las pruebas con Kubernetes, como el espacio de nombres (*namespace*) del proyecto. El backend remoto de Terraform deberá configurarse según la solución acordada por el equipo.

### 3. Imagen base Docker del backend

Se utilizará **`node:20-alpine`** como imagen base para construir el contenedor del backend.

Esta imagen proporciona el entorno de Node.js necesario para ejecutar la aplicación y utiliza Alpine Linux como base, lo que permite mantener una imagen ligera en comparación con imágenes más completas.

La imagen deberá utilizarse de manera consistente en el Dockerfile del backend y la construcción del contenedor deberá seguir prácticas que permitan obtener imágenes reproducibles.

## Alternativas consideradas

### Kubernetes

- **Minikube:** permite ejecutar Kubernetes localmente y es útil para aprendizaje y desarrollo.
- **Kind:** permite crear clústeres Kubernetes utilizando contenedores Docker como nodos.
- **K3d:** permite ejecutar K3s dentro de contenedores Docker y crear entornos locales de manera práctica.

Se selecciona K3d por su enfoque en la ejecución de clústeres K3s dentro de Docker y su utilidad para realizar pruebas locales.

### Infraestructura como Código

- **Terraform:** permite definir infraestructura mediante archivos declarativos y cuenta con soporte para distintos proveedores.
- **Pulumi:** permite definir infraestructura utilizando lenguajes de programación como TypeScript, Python y Go.
- **CloudFormation:** permite administrar infraestructura de AWS mediante plantillas.

Se selecciona Terraform por su configuración declarativa, su ecosistema y su capacidad para administrar infraestructura mediante código.

### Imagen base Docker

Se selecciona `node:20-alpine` por proporcionar Node.js y una base Linux ligera para ejecutar el backend.

## Consecuencias

### Positivas

- Se podrá probar Kubernetes localmente sin necesitar inicialmente un clúster administrado en la nube.
- El equipo podrá reproducir el entorno de pruebas utilizando K3d y Docker.
- Terraform permitirá mantener la configuración de infraestructura versionada y documentada.
- La imagen base seleccionada permitirá construir el contenedor del backend utilizando Node.js.
- Las configuraciones podrán mantenerse en el repositorio junto con el resto del proyecto.

### Negativas y consideraciones

- Los resultados de las pruebas locales pueden diferir de los de un entorno de producción.
- El equipo deberá instalar y configurar Docker, K3d, kubectl y Terraform.
- La infraestructura deberá mantenerse actualizada y las configuraciones deberán validarse antes de aplicarse.
- El estado de Terraform deberá almacenarse de forma segura, preferentemente en un backend remoto con bloqueo cuando sea compatible. No se deberán subir archivos de estado que contengan información sensible al repositorio.
- La imagen base y sus dependencias deberán mantenerse actualizadas y revisarse por posibles vulnerabilidades.

## Alcance

Esta decisión establece K3d como plataforma local de pruebas, Terraform como herramienta de Infraestructura como Código y `node:20-alpine` como imagen base del backend.

La selección de K3d para las pruebas no implica por sí sola migrar MediTriage a Kubernetes en producción. La plataforma de despliegue debe mantenerse alineada con las decisiones arquitectónicas previamente aceptadas por el equipo.

## Referencias

- Presentación S07: Contenedores, Kubernetes e Infraestructura como Código.
- ADR anteriores de MediTriage relacionados con la arquitectura y la plataforma de despliegue.
