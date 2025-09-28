variable "cidr_block" {
  type = string
}
variable "subnet_cidr_block" {
  type = string
}
variable "availability_zone" {
  type = string
}
variable "tags" {
  type = map(string)
}
variable "ec2_ami" {
  type = string
}
variable "ec2_instance_type" {
  type = string
}
variable "rds_identifier" {
  type = string
}
variable "rds_instance_class" {
  type = string
}
variable "rds_engine" {
  type = string
}
variable "rds_username" {
  type = string
}
variable "rds_password" {
  type = string
}
