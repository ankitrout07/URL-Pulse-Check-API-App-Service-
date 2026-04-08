variable "project_name" {
  description = "Name of the project"
  default     = "pulse-check"
}

variable "location" {
  description = "Azure region"
  default     = "East US"
}

variable "db_admin_user" {
  description = "Database administrator username"
  default     = "pulseadmin"
}

variable "db_password" {
  description = "Database administrator password"
  sensitive   = true
}
