data "aws_iam_role" "chalice" {
  name = "fileUpload-dev"

  depends_on = [
    aws_iam_role.default-role,
  ]
}


data "aws_iam_policy_document" "fileuploader" {
  statement {
    actions = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:Scan",
      "dynamodb:DeleteItem",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    actions = [
      "kms:*"
    ]

    resources = [
      "*",
    ]
  }

  statement {
    actions = [
      "s3:*",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_policy" "uploader_policy" {
  name   = "serverless_file_uploader"
  path   = "/"
  policy = data.aws_iam_policy_document.fileuploader.json

  depends_on = [
    aws_iam_role.default-role,
  ]
}


resource "aws_iam_policy_attachment" "test-attach" {
  name       = "test-attachment"
  roles      = [data.aws_iam_role.chalice.name]
  policy_arn = aws_iam_policy.uploader_policy.arn

  depends_on = [
    aws_iam_role.default-role,
  ]
}
