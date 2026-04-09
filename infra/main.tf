terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.project_name}-rg"
  location = var.location
}

# App Service Plan
resource "azurerm_service_plan" "plan" {
  name                = "${var.project_name}-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "B1"
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "db" {
  name                   = "${var.project_name}-db-server"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "14"
  administrator_login    = var.db_admin_user
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
}

# App Service
resource "azurerm_linux_web_app" "app" {
  name                = "${var.project_name}-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    application_stack {
      python_version = "3.11"
    }
    app_command_line = "uvicorn app.main:app --host 0.0.0.0 --port 8000"
  }

  app_settings = {
    "DATABASE_URL"                    = "postgresql://${var.db_admin_user}:${var.db_password}@${azurerm_postgresql_flexible_server.db.fqdn}:5432/postgres?sslmode=require"
    "SCM_DO_BUILD_DURING_DEPLOYMENT"  = "false"
    "WEBSITE_RUN_FROM_PACKAGE"        = "0"
  }
}

# Firewall rule to allow Azure Services (the App Service) to access the DB
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure" {
  name             = "allow-azure-services"
  server_id        = azurerm_postgresql_flexible_server.db.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
resource "azurerm_postgresql_flexible_server" "db" {
  name                   = "pulse-check-db"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  
  # Ensure this zone is either the current standby zone 
  # or match the existing primary zone in the portal
  zone                   = "1" 

  high_availability {
    mode                      = "ZoneRedundant"
    standby_availability_zone = "2"
  }
  
  # ... other settings
}