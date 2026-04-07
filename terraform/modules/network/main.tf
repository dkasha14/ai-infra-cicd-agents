provider "aws" {
  region = "us-west-2"
}
resource "aws_vpc" "dlr-vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "dlr-vpc"
  }
}
resource "aws_internet_gateway" "dlr-igw" {
  vpc_id = aws_vpc.dlr-vpc.id
  tags = {
    Name = "dlr-igw"
  }
}
resource "aws_subnet" "dlr-public-subnet-1" {
  vpc_id            = aws_vpc.dlr-vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-west-2a"
  tags = {
    Name = "dlr-public-subnet-1"
  }
}
resource "aws_subnet" "dlr-public-subnet-2" {
  vpc_id            = aws_vpc.dlr-vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-west-2b"
  tags = {
    Name = "dlr-public-subnet-2"
  }
}
resource "aws_subnet" "dlr-private-subnet-1" {
  vpc_id            = aws_vpc.dlr-vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-west-2a"
  tags = {
    Name = "dlr-private-subnet-1"
  }
}
resource "aws_subnet" "dlr-private-subnet-2" {
  vpc_id            = aws_vpc.dlr-vpc.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-west-2b"
  tags = {
    Name = "dlr-private-subnet-2"
  }
}
resource "aws_route_table" "dlr-public-rt" {
  vpc_id = aws_vpc.dlr-vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.dlr-igw.id
  }
  tags = {
    Name = "dlr-public-rt"
  }
}
resource "aws_route_table_association" "dlr-public-subnet-1" {
  subnet_id      = aws_subnet.dlr-public-subnet-1.id
  route_table_id = aws_route_table.dlr-public-rt.id
}
resource "aws_route_table_association" "dlr-public-subnet-2" {
  subnet_id      = aws_subnet.dlr-public-subnet-2.id
  route_table_id = aws_route_table.dlr-public-rt.id
}
output "vpc_id" {
  value = aws_vpc.dlr-vpc.id
}
output "public_subnet_ids" {
  value = [aws_subnet.dlr-public-subnet-1.id, aws_subnet.dlr-public-subnet-2.id]
}
output "private_subnet_ids" {
  value = [aws_subnet.dlr-private-subnet-1.id, aws_subnet.dlr-private-subnet-2.id]
}
