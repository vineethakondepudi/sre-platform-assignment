variable "service_name" {
  type = string
}

# Placeholder module to represent K8s manifest generation in a real platform
output "info" {
  value = "Kubernetes templates would be generated for ${var.service_name}"
}
