output "webapp_url" {
  value       = "https://${azurerm_linux_web_app.app.default_hostname}"
  description = "The URL of the deployed App Service"
}

output "webapp_name" {
  value       = azurerm_linux_web_app.app.name
  description = "The exact name of the Web App"
}

output "postgresql_fqdn" {
  value       = azurerm_postgresql_flexible_server.db.fqdn
}
