terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }

    template = {
      version = "~> 2"
      source  = "hashicorp/template"
    }

    null = {
      version = "~> 2"
      source  = "hashicorp/null"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-west-1"
}
