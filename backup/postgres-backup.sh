#!/bin/bash

# Set the backup directory
backup_dir="$HOME/backups"

# HAPI FHIR database credentials
hapi_username="admin"
hapi_password="instant101"
hapi_database="hapi"

# Function to backup a PostgreSQL database
backup_database() {
    local container_id="$1"
    local db_name="$2"
    local username="$3"
    local password="$4"
    local backup_file="$backup_dir/$db_name-$(date +%Y-%m-%d_%H-%M-%S).sql"
    docker exec -t "$container_id" env PGPASSWORD="$password" pg_dump -U "$username" -d "$db_name" > "$backup_file"
    echo "Backup for database $db_name created at $backup_file"
}

# Function to rotate backups
rotate_backups() {
    local retention_period="$1"
    find "$backup_dir" -name "*.sql" -type f -mtime +"$retention_period" -delete
    echo "Old backups older than $retention_period days have been deleted."
}

# Backup HAPI FHIR database
backup_hapi_fhir_database() {
    local container_id=$(docker ps --format '{{.ID}}' --filter name=hapi-fhir_postgres)
    if [ -n "$container_id" ]; then
        backup_database "$container_id" "$hapi_database" "$hapi_username" "$hapi_password"
    else
        echo "HAPI FHIR container not found."
    fi
}


# Backup specific containers
backup_hapi_fhir_database
rotate_backups 30