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
