terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "aws" {
  region = var.aws_region
  
  # Recommended: authenticate via AWS CLI:
  # run `aws configure` locally before `terraform apply`
  # OR set environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
}
