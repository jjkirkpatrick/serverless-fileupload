data "aws_iam_role" "chalice" {
  name = "fileUpload-dev"

  depends_on = [
    aws_iam_role.default-role,
  ]
}


data "aws_iam_policy_document" "fileuploader" {
  statement {
    sid = "1"

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
    sid = "2"

    actions = [
      "s3:*",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_policy" "example" {
  name   = "fileuploaderpolicy"
  path   = "/"
  policy = data.aws_iam_policy_document.fileuploader.json

  depends_on = [
    aws_iam_role.default-role,
  ]
}


resource "aws_iam_policy_attachment" "test-attach" {
  name       = "test-attachment"
  roles      = [data.aws_iam_role.chalice.name]
  policy_arn = aws_iam_policy.example.arn

  depends_on = [
    aws_iam_role.default-role,
  ]
}
