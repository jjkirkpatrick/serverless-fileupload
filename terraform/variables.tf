variable "create_website_route53_record" {
  type        = bool
  default     = true
}

variable "create_api_route53_record" {
  type        = bool
  default     = true
}

variable "domain_name" {
  type        = string
}

variable "api_subdomain" {
  type        = string
}

variable "website_bucket_name" {
  type        = string
}

variable "uploaded_files_bucket_name" {
  type        = string
}
