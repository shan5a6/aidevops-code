resource "aws_vpc" "myvpc" {
  cidr_block           = "172.31.0.0/16"
  enable_dns_hostnames = "true"
  enable_dns_support   = "true"
  instance_tenancy     = "default"
  region               = "us-west-2"
}


resource "aws_subnet" "sub1" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = "172.31.32.0/20"
  enable_dns64                                   = "false"
  enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
  map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  region                                         = "us-west-2"
  vpc_id                                         = "${data.terraform_remote_state.vpc.outputs.aws_vpc_tfer--vpc-030874a8eadd391a7_id}


resource "aws_subnet" "tfer--subnet-00cccba6d462bcfbe" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = "172.31.48.0/20"
  enable_dns64                                   = "false"
  enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
  map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  region                                         = "us-west-2"
  vpc_id                                         = "${data.terraform_remote_state.vpc.outputs.aws_vpc_tfer--vpc-030874a8eadd391a7_id}


resource "aws_subnet" "tfer--subnet-09cd4116d91256d46" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = "172.31.16.0/20"
  enable_dns64                                   = "false"
  enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
  map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  region                                         = "us-west-2"
  vpc_id                                         = "${data.terraform_remote_state.vpc.outputs.aws_vpc_tfer--vpc-030874a8eadd391a7_id}


resource "aws_subnet" "tfer--subnet-0f9792457f96a5f29" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = "172.31.0.0/20"
  enable_dns64                                   = "false"
  enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
  map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  region                                         = "us-west-2"
  vpc_id                                         = "${data.terraform_remote_state.vpc.outputs.aws_vpc_tfer--vpc-030874a8eadd391a7_id}
