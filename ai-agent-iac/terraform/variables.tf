variable "region" {
  type        = string
  default     = "us-west-2"
}

variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  type        = string
  default     = "us-west-2a"
}

variable "ami" {
  type        = string
  default     = "ami-0c94855ba95c71c99"
}

variable "instance_type" {
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  type        = string
  default     = "example-key"
}
