terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}

  subscription_id = "00000000-0000-0000-0000-000000000000"
}

variable "storage_account_name" {
    default = "skuvault"
}
variable "container_env" {
    type = list(string)
    default = ["dev", "test", "live"]
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.storage_account_name}-rg"
  location = "eastus"
}

resource "azurerm_storage_account" "sa" {
  name                     = "${var.storage_account_name}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_kind             = "BlobStorage"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "containers" {
  for_each = { for name in var.container_names: name => name}
  name                  = each.value
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}


resource "azurerm_storage_blob" "data_blob" {
  for_each = { for name in var.container_names: name => name}  
  name                   = "my-awesome-content.json"
  storage_account_name   = azurerm_storage_account.sa.name
  storage_container_name = azurerm_storage_container.containers.name
  type                   = "Block"
  source                 = "logs.json"
  access_tier            = each.key == "live" ? "Cool" : "Archive"

}

resource "azurerm_storage_management_policy" "sapolicy" {
    storage_account_id = azurerm_storage_account.sa.id
    rule {
    name    = "retention"
    enabled = true
    filters {
      prefix_match = ["dev/prefix1", "test/prefix2"]
      blob_types   = ["blockBlob"]
    }
    actions {
      base_blob {
        delete_after_days_since_modification_greater_than          = 14
      }
    }
  }
}