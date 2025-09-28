resource "aws_db_instance" "this" {
  identifier = var.identifier
  instance_class = var.instance_class
  engine = var.engine
  username = var.username
  password = var.password
  vpc_security_group_ids = [var.security_group_id]
  db_subnet_group_name = aws_db_subnet_group.this.id
}
resource "aws_db_subnet_group" "this" {
  name       = var.identifier
  subnet_ids = [var.subnet_id]
}
