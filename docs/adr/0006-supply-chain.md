# ADR-0006: Política de Firma de Artefactos, Provenance SLSA Nivel 2 y Control de Admisión en Cadena de Suministro

* **Estado:** Aceptado
* **Fecha:** 2026-11-14
* **Contexto del Proyecto:** MediTriage (HealthTech)
* **Sesión:** S10 — DevSecOps II: Supply Chain Security

---

## 1. Contexto y Problema

En una plataforma HealthTech como **MediTriage**, que procesa datos clínicos sensibles sujetos a normativas de privacidad y cumplimiento (Ley 19.628 / Ley 21.719) y exige una disponibilidad del 99.5%, proteger el código fuente mediante controles shift-left (SAST, SCA y escaneo de secretos en S09) no es suficiente si la cadena de suministro de compilación y despliegue puede ser comprometida.

Incidentes de la industria como SolarWinds y XZ Utils demuestran que un atacante puede inyectar artefactos maliciosos entre la fase de construcción (build) y el entorno de ejecución (runtime), o desplegar imágenes no autorizadas directamente en el clúster. Necesitamos garantizar criptográficamente que:
1. Toda imagen de contenedor publicada en GitHub Container Registry (`ghcr.io`) provenga exclusivamente de nuestro pipeline oficial de CI/CD en GitHub Actions.
2. Exista trazabilidad auditable del origen y proceso de construcción del artefacto (provenance).
3. El clúster de Kubernetes rechace automáticamente cualquier intento de ejecutar imágenes no firmadas o alteradas.

---

## 2. Decisión Arquitectónica

Adoptamos una arquitectura de seguridad de cadena de suministro basada en tres pilares obligatorios:

### A. Política de Firma Criptográfica: Cosign con Keyless Signing (Sigstore + OIDC)
* **Herramienta:** **Cosign** (parte del proyecto Sigstore).
* **Modalidad:** **Keyless signing** mediante federación de identidad OIDC nativa de GitHub Actions (`https://token.actions.githubusercontent.com`).
* **Justificación:** Evita el riesgo operativo de almacenar, proteger y rotar claves privadas de larga duración (PATs o llaves GPG) en los secretos del repositorio. En su lugar, Fulcio emite certificados efímeros de corta duración vinculados criptográficamente a la identidad del workflow de GitHub Actions que construyó la imagen, y el evento queda registrado de forma inmutable en el log de transparencia **Rekor**.
* **Verificación en Pipeline:** Inmediatamente después de firmar por digest inmutable (`@sha256`), el job ejecuta `cosign verify` validando el emisor OIDC y la identidad del repositorio antes de permitir la promoción o pruebas dinámicas (DAST).

### B. Nivel de Madurez y Trazabilidad: SLSA Nivel 2 (Supply-chain Levels for Software Artifacts)
* **Nivel elegido:** **SLSA Nivel 2**.
* **Implementación:** Generación y adjunción de atestaciones de procedencia firmadas (`slsaprovenance`) sobre el digest de la imagen publicada en `ghcr.io` mediante `cosign attest --type slsaprovenance` / `actions/attest-build-provenance`.
* **Justificación:** SLSA Nivel 2 garantiza que la construcción se ejecuta en un servicio de CI hospedado (GitHub Actions) y produce una atestación de procedencia autenticada y firmada que vincula el binario final con el commit exacto (`github.sha`), el repositorio y el workflow que lo generó. Esto cubre nuestros requerimientos de auditoría sin el sobrecosto de infraestructura que exige SLSA Nivel 3 (runners aislados dedicados no estándar) en esta etapa del MVP.

### C. Prevención en Admisión y Vigilancia en Runtime: Kyverno + Falco
* **Control preventivo (Admission Time):** **Kyverno** mediante la política `k8s/policies/require-signature.yaml` en modo `Enforce`. El admission controller intercepta toda creación de `Pod` en el clúster e impide la admisión de cualquier imagen de `ghcr.io` que no posea una firma válida de Cosign emitida por nuestro workflow oficial y su correspondiente attestation SLSA Nivel 2.
* **Control detectivo (Runtime Security):** **Falco** instrumentado con sondas eBPF (`falco/rules-custom.yaml`) para detectar comportamientos anómalos posdespliegue (como apertura de shells interactivas en contenedores, escrituras fuera de directorios de datos autorizados o conexiones salientes sospechosas).
* **Retención y Cumplimiento:** En línea con los requisitos de trazabilidad regulatoria de MediTriage, las firmas criptográficas y las attestations SLSA se conservan junto a cada imagen en el registro mientras esté en uso y se respaldan por un período de **5 años**.

---

## 3. Alternativas Consideradas

| Alternativa | Motivo de descarte |
| :--- | :--- |
| **Firma con claves estáticas (Cosign con par de llaves local/KMS o Docker Content Trust / Notary v1)** | Introduce carga operativa de rotación de secretos y riesgo de filtración de la clave privada en CI. Keyless signing con OIDC elimina los secretos de larga duración. |
| **SLSA Nivel 1** | Solo exige un proceso de build documentado, pero no ofrece provenance firmada criptográficamente, por lo que no previene adulteraciones ni permite verificación automática en admisión. |
| **SLSA Nivel 3** | Aunque ofrece garantías superiores contra manipulación del entorno de build, requiere plataformas con aislamiento reforzado y runners efímeros endurecidos que exceden el alcance del entorno actual del equipo. |
| **OPA Gatekeeper para control de admisión** | Requiere escribir y mantener políticas en lenguaje Rego. Elegimos **Kyverno** porque permite definir políticas nativas en YAML (`verifyImages`) con integración directa para verificar firmas Cosign y attestations OIDC. |

---

## 4. Consecuencias

### Positivas
* **Cero secretos de firma en CI:** No existen llaves privadas que puedan ser robadas del repositorio.
* **Bloqueo automático de despliegues manuales o alterados:** Ningún desarrollador o atacante puede desplegar en el clúster una imagen compilada localmente que no haya pasado todos los quality gates y el job `sign_and_attest` del pipeline.
* **Trazabilidad completa para auditoría:** Cada contenedor en ejecución puede rastrearse criptográficamente hasta el commit, autor y ejecución exacta del pipeline por 5 años.

### Negativas / Trade-offs
* **Dependencia de infraestructura externa en el despliegue:** La verificación keyless en admisión requiere conectividad hacia la infraestructura de Sigstore (Rekor/Fulcio) o caché de certificados en el clúster.
* **Mayor tiempo de ejecución del pipeline:** La generación de firmas, atestaciones y verificación añade pasos adicionales antes del despliegue a staging y las pruebas DAST.
