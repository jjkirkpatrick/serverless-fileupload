data "aws_route53_zone" "selected" {
  name         = var.domain_name
  private_zone = false
}

resource "aws_route53_record" "api_gateway_alias" {
  zone_id = data.aws_route53_zone.selected.zone_id
  name    = "${var.api_subdomain}.${data.aws_route53_zone.selected.name}"
  type    = "A"

  alias {
    name                   = aws_api_gateway_domain_name.api_gateway_custom_domain.cloudfront_domain_name
    zone_id                = aws_api_gateway_domain_name.api_gateway_custom_domain.cloudfront_zone_id
    evaluate_target_health = false
  }

}

resource "aws_route53_record" "s3_bucket_alias" {
  zone_id = data.aws_route53_zone.selected.zone_id
  name    = data.aws_route53_zone.selected.name
  type    = "A"

  alias {
    name                   = module.s3_bucket.this_s3_bucket_website_domain
    zone_id                = module.s3_bucket.this_s3_bucket_hosted_zone_id
    evaluate_target_health = false
  }

}