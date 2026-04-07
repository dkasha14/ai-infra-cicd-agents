variable "instance_type" {
  default = "t2.micro"
}
variable "ami" {
  default = "ami-0c94855ba95c71c99"
}
variable "vpc_id" {
}
variable "public_subnets" {
  type = list
}
variable "private_subnets" {
  type = list
}
variable "security_group_id" {
}
resource "aws_instance" "asha_ec2" {
  ami = var.ami
  instance_type = var.instance_type
  vpc_security_group_ids = [var.security_group_id]
  subnet_id = var.public_subnets[0]
  tags = {
    Project = "iac-agents"
    Environment = "dev"
  }
}
output "instance_id" {
  value = aws_instance.asha_ec2.id
}
