provider "aws" {
  region = "us-west-2"
}
resource "aws_s3_bucket" "dlr-bucket" {
  bucket = "dlr-bucket"
  acl    = "private"
  tags = {
    Name = "dlr-bucket"
  }
}
