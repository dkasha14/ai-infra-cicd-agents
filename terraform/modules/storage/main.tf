variable "bucket_name" {
  default = "asha-bucket"
}
resource "aws_s3_bucket" "asha_bucket" {
  bucket = var.bucket_name
  tags = {
    Project = "iac-agents"
    Environment = "dev"
  }
}
output "bucket_name" {
  value = aws_s3_bucket.asha_bucket.id
}
