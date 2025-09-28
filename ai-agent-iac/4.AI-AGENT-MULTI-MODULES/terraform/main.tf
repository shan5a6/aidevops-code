module "vpc" {
  source = "./modules/vpc"
  cidr_block = var.cidr_block
  subnet_cidr_block = var.subnet_cidr_block
  availability_zone = var.availability_zone
  tags = var.tags
}
module "ec2" {
  source = "./modules/ec2"
  ami = var.ec2_ami
  instance_type = var.ec2_instance_type
  subnet_id = module.vpc.subnet_id
  security_group_id = module.vpc.security_group_id
  tags = var.tags
}
module "rds" {
  source = "./modules/rds"
  identifier = var.rds_identifier
  instance_class = var.rds_instance_class
  engine = var.rds_engine
  username = var.rds_username
  password = var.rds_password
  subnet_id = module.vpc.subnet_id
  security_group_id = module.vpc.security_group_id
}
