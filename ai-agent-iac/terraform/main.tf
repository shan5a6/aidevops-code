provider "aws" {
  region = var.region
}

resource "aws_vpc" "example" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = "example-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.example.id
  cidr_block        = var.public_subnet_cidr
  availability_zone = var.availability_zone
  tags = {
    Name = "public-subnet"
  }
}

resource "aws_internet_gateway" "example" {
  vpc_id = aws_vpc.example.id
  tags = {
    Name = "example-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.example.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.example.id
  }
  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "example" {
  name        = "example-sg"
  description = "Allow inbound traffic on port 22 and 80"
  vpc_id      = aws_vpc.example.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "example-sg"
  }
}

resource "aws_instance" "example" {
  ami           = var.ami
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.example.id]
  key_name               = var.key_name
  tags = {
    Name = "example-ec2"
  }
}
