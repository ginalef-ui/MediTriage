# 1. Configuración de Terraform y Backend Remoto
terraform {
  required_version = ">= 1.6" # Requisito del mini-lab
  
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }

  # Backend remoto (Ejemplo con AWS S3 y DynamoDB)

}

# 2. Provider
provider "kubernetes" {
  config_path = "~/.kube/config" # Apunta a tu clúster local (Docker Desktop, kind, etc.)
}

# 3. Creación del Namespace
resource "kubernetes_namespace" "equipo_namespace" {
  metadata {
    name = "nombre-de-tu-equipo"
  }
}

# 4. Secret Placeholder
resource "kubernetes_secret" "app_secret_placeholder" {
  metadata {
    name      = "app-secrets"
    namespace = kubernetes_namespace.equipo_namespace.metadata[0].name
  }

  data = {
    API_KEY = "placeholder-value"
  }

  type = "Opaque"
}
