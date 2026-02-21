provider "aws" {
  region = "us-east-1"
}

variable "service_name" {
  type = string
}

module "ecr" {
  source       = "./modules/ecr"
  service_name = var.service_name
}

module "iam" {
  source       = "./modules/iam"
  service_name = var.service_name
}

# This module represents generation of K8s manifests/templates in a real IDP
module "k8s_template" {
  source       = "./modules/k8s-template"
  service_name = var.service_name
}
