locals {
  upload_bucket = join("-",[var.uploaded_files_bucket_name,random_id.upload_bucket.hex])
}


######################
##### S3 website #####
######################

resource "aws_kms_key" "objects" {
  description             = "KMS key is used to encrypt bucket objects"
  deletion_window_in_days = 7
}

module "s3_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = var.website_bucket_name
  acl    = "private"

  versioning = {
    enabled = true
  }

  attach_policy = true
  policy        = data.aws_iam_policy_document.website_bucket_policy.json

  website = {
    index_document = "index.html"
    error_document = "index.html"
  }

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        sse_algorithm     = "AES256"
      }
    }
  }
}

data "aws_iam_policy_document" "website_bucket_policy" {
  statement {
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
    ]

    resources = [
      "arn:aws:s3:::${var.website_bucket_name}/*",
    ]
  }
}

###########################
##### Uploaded assets #####
###########################



resource "aws_kms_key" "uploaded_assets" {
  description             = "KMS key is used to encrypt bucket objects"
  deletion_window_in_days = 7
}

module "s3_bucket_file_storage" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket = local.upload_bucket
  acl    = "private"

  versioning = {
    enabled = false
  }

  cors_rule = [
    {
      allowed_methods = ["POST"]
      allowed_origins = ["https://${var.domain_name}", "http://${var.domain_name}"]
      allowed_headers = ["*"]
      expose_headers  = []
      }
  ]

  server_side_encryption_configuration = {
    rule = {
      apply_server_side_encryption_by_default = {
        kms_master_key_id = aws_kms_key.uploaded_assets.arn
        sse_algorithm     = "aws:kms"
      }
    }
  }

}


resource "random_id" "upload_bucket" {
  keepers = {
    # Generate a new id each time we switch to a new AMI id
    bucket = var.uploaded_files_bucket_name
  }

  byte_length = 8
}
