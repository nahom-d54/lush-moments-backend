#!/usr/bin/env python3
"""
Lush Moments Management CLI

A Django-style management interface for database operations.

Usage:
    python manage.py <command> [options]

Commands:
    all              - Seed all tables with sample data
    fresh            - Drop all tables and reseed (⚠️  destructive)
    table <name>     - Seed a specific table
    drop             - Drop all database tables (⚠️  destructive)
    createsuperuser  - Create an admin user interactively
    create-tables    - Create database tables without seeding
    list             - List all available tables
    info             - Show default credentials and data info

Examples:
    python manage.py all
    python manage.py fresh --force
    python manage.py table users
    python manage.py createsuperuser
    python manage.py createsuperuser --email admin@test.com --name "Admin"
    python manage.py list
"""

from app.seeders.cli import app

if __name__ == "__main__":
    app()
