variable "location" {
  type    = string
  default = "West US"
}
variable "resource_group_name" {
  type    = string
  default = "myresourcegroup"
}
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}
resource "azurerm_virtual_network" "vn" {
  name                = "myvirtualnetwork"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
}
resource "azurerm_subnet" "sn" {
  name                 = "mysubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vn.name
  address_prefixes     = ["10.0.1.0/24"]
}
resource "azurerm_network_interface" "ni" {
  name                = "mynetworkinterface"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  ip_configuration {
    name                          = "myipconfiguration"
    subnet_id                     = azurerm_subnet.sn.id
    private_ip_address_allocation = "Dynamic"
  }
}
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}
output "network_interface_id" {
  value = azurerm_network_interface.ni.id
}
