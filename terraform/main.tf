provider "aws" {
  region = "us-west-2"
}
module "network" {
  source = "./modules/network"
}
module "compute" {
  source       = "./modules/compute"
  vpc_id       = module.network.vpc_id
  public_subnets = module.network.public_subnets
  private_subnets = module.network.private_subnets
  security_group_id = module.network.security_group_id
}
module "storage" {
  source = "./modules/storage"
}
