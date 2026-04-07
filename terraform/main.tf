provider "azurerm" {
  features {}
}
module "network" {
  source = "./modules/network"
}
module "compute" {
  source               = "./modules/compute"
  resource_group_name  = module.network.resource_group_name
  network_interface_id = module.network.network_interface_id
}
