variable "resource_group_name" {
  type = string
}
variable "network_interface_id" {
  type = string
}
variable "admin_username" {
  type    = string
  default = "adminuser"
}
variable "admin_password" {
  type    = string
  default = "P@ssw0rd1234!"
}
resource "azurerm_linux_virtual_machine" "vm" {
  name                = "mylinuxvirtualmachine"
  resource_group_name = var.resource_group_name
  location            = "West US"
  size                = "Standard_DS2_v2"
  admin_username      = var.admin_username
  admin_password      = var.admin_password
  network_interface_ids = [
    var.network_interface_id
  ]
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "16.04-LTS"
    version   = "latest"
  }
}
