variable "vpc_cidr" {
  default = "10.0.0.0/16"
}
variable "public_subnet_cidrs" {
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}
variable "private_subnet_cidrs" {
  default = ["10.0.3.0/24", "10.0.4.0/24"]
}
resource "aws_vpc" "asha_vpc" {
  cidr_block = var.vpc_cidr
  tags = {
    Project = "iac-agents"
    Environment = "dev"
  }
}
resource "aws_internet_gateway" "asha_igw" {
  vpc_id = aws_vpc.asha_vpc.id
  tags = {
    Project = "iac-agents"
    Environment = "dev"
  }
}
resource "aws_subnet" "asha_public_subnets" {
  count = length(var.public_subnet_cidrs)
  vpc_id = aws_vpc.asha_vpc.id
  cidr_block = var.public_subnet_cidrs[count.index]
  availability_zone = "us-west-2${count.index % 2 + 1}"
  tags = {
    Project = "iac-agents"
    Environment = "dev"
  }
}
resource "aws_subnet" "asha_private_subnets" {
  count = length(var.private_subnet_cidrs)
  vpc_id = aws_vpc.asha_vpc.id
  cidr_block = var.private_subnet_cidrs[count.index]
  availability_zone = "us-west-2${count.index % 2 + 1}"
  tags = {
    Project = "iac-agents"
    Environment = "dev"
  }
}
resource "aws_route_table" "asha_public_rt" {
  vpc_id = aws_vpc.asha_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.asha_igw.id
  }
  tags = {
    Project = "iac-agents"
    Environment = "dev"
  }
}
resource "aws_route_table_association" "asha_public_rt_assoc" {
  count = length(var.public_subnet_cidrs)
  subnet_id = aws_subnet.asha_public_subnets[count.index].id
  route_table_id = aws_route_table.asha_public_rt.id
}
resource "aws_security_group" "asha_sg" {
  vpc_id = aws_vpc.asha_vpc.id
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Project = "iac-agents"
    Environment = "dev"
  }
}
output "vpc_id" {
  value = aws_vpc.asha_vpc.id
}
output "public_subnets" {
  value = aws_subnet.asha_public_subnets.*.id
}
output "private_subnets" {
  value = aws_subnet.asha_private_subnets.*.id
}
output "security_group_id" {
  value = aws_security_group.asha_sg.id
}
