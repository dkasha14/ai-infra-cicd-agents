provider "aws" {
  region = "us-west-2"
}
module "network" {
  source = "./modules/network"
}
module "compute" {
  source = "./modules/compute"
  vpc_id = module.network.vpc_id
  public_subnet_ids = module.network.public_subnet_ids
  private_subnet_ids = module.network.private_subnet_ids
  security_group_id = module.compute.security_group_id
}
module "storage" {
  source = "./modules/storage"
}
