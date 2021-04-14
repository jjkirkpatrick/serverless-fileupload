resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "fileuploadlookup"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "uri"

  attribute {
    name = "uri"
    type = "S"
  }

}
