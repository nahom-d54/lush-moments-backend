#!/usr/bin/env python3
"""
Database Seeder CLI - Interactive seeding utility using Typer

A Django-style management command for database seeding operations.
"""

import asyncio
from enum import Enum
from getpass import getpass
from typing import Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from sqlalchemy import select

from app.database import AsyncSessionLocal, Base, engine
from app.models import User
from app.seeders.seed_new import (
    clear_tables,
    create_tables,
    seed_all,
    seed_contact_info,
    seed_contact_messages,
    seed_gallery,
    seed_packages,
    seed_sample_bookings,
    seed_testimonials,
    seed_themes,
    seed_translations,
    seed_users,
)
from app.utils.auth import get_password_hash

app = typer.Typer(
    name="Lush Moments Seeder",
    help="Database seeding and management commands",
    add_completion=False,
)
console = Console()


class TableName(str, Enum):
    """Available tables for seeding"""

    users = "users"
    packages = "packages"
    gallery = "gallery"
    contact_info = "contact_info"
    contact_messages = "contact_messages"
    themes = "themes"
    testimonials = "testimonials"
    bookings = "bookings"
    translations = "translations"


# Table name to seeder function mapping
SEEDERS = {
    TableName.users: seed_users,
    TableName.packages: seed_packages,
    TableName.gallery: seed_gallery,
    TableName.contact_info: seed_contact_info,
    TableName.contact_messages: seed_contact_messages,
    TableName.themes: seed_themes,
    TableName.testimonials: seed_testimonials,
    TableName.bookings: seed_sample_bookings,
    TableName.translations: seed_translations,
}


@app.command("all")
def seed_all_tables(
    skip_existing: bool = typer.Option(
        True, "--skip-existing/--force", help="Skip tables that already have data"
    ),
):
    """
    Seed all database tables with sample data.

    Creates tables if they don't exist and populates them with initial data.
    """
    console.print("\n[bold cyan]🌱 Seeding all tables...[/bold cyan]\n")

    async def run():
        await create_tables()
        await seed_all()

    asyncio.run(run())
    console.print("\n[bold green]✅ All tables seeded successfully![/bold green]\n")


@app.command("fresh")
def fresh_seed(
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation prompt"),
):
    """
    Drop all tables and reseed the database.

    ⚠️  WARNING: This will delete ALL existing data!
    """
    if not force:
        console.print(
            Panel(
                "[bold red]⚠️  WARNING: This will DROP ALL TABLES and DELETE ALL DATA![/bold red]\n\n"
                "All existing data will be permanently lost.",
                title="Destructive Operation",
                border_style="red",
            )
        )

        confirmed = Confirm.ask("Are you sure you want to continue?", default=False)
        if not confirmed:
            console.print("[yellow]❌ Operation cancelled[/yellow]")
            raise typer.Abort()

    console.print("\n[bold yellow]🗑️  Dropping all tables...[/bold yellow]")

    async def run():
        await clear_tables()
        console.print("[bold cyan]🌱 Seeding fresh data...[/bold cyan]\n")
        await seed_all()

    asyncio.run(run())
    console.print("\n[bold green]✅ Database reset successfully![/bold green]\n")


@app.command("table")
def seed_table(
    table_name: TableName = typer.Argument(..., help="Name of the table to seed"),
):
    """
    Seed a specific table with sample data.

    Available tables: users, packages, gallery, contact_info, contact_messages,
    themes, testimonials, bookings, translations
    """
    console.print(f"\n[bold cyan]🌱 Seeding {table_name.value}...[/bold cyan]\n")

    async def run():
        await create_tables()
        await SEEDERS[table_name]()

    asyncio.run(run())
    console.print(
        f"\n[bold green]✅ {table_name.value} seeded successfully![/bold green]\n"
    )


@app.command("drop")
def drop_tables(
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation prompt"),
):
    """
    Drop all database tables.

    ⚠️  WARNING: This will delete ALL data!
    """
    if not force:
        console.print(
            Panel(
                "[bold red]⚠️  WARNING: This will DROP ALL TABLES![/bold red]\n\n"
                "All data will be permanently lost.",
                title="Destructive Operation",
                border_style="red",
            )
        )

        confirmed = Confirm.ask("Are you sure you want to continue?", default=False)
        if not confirmed:
            console.print("[yellow]❌ Operation cancelled[/yellow]")
            raise typer.Abort()

    console.print("\n[bold yellow]🗑️  Dropping all tables...[/bold yellow]")

    async def run():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(run())
    console.print("\n[bold green]✅ All tables dropped successfully![/bold green]\n")


@app.command("createsuperuser")
def create_superuser(
    email: Optional[str] = typer.Option(None, "--email", "-e", help="Admin email"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Admin name"),
    phone: Optional[str] = typer.Option(None, "--phone", "-p", help="Phone number"),
):
    """
    Create a superuser (admin) account interactively.

    Similar to Django's createsuperuser command.
    """
    console.print(
        Panel(
            "[bold cyan]Create a new admin user[/bold cyan]",
            title="🔐 Create Superuser",
            border_style="cyan",
        )
    )
    console.print()

    async def run():
        async with AsyncSessionLocal() as db:
            # Get email
            user_email = email
            while True:
                if not user_email:
                    user_email = Prompt.ask("[bold]Email address[/bold]").strip()

                if not user_email:
                    console.print("[red]❌ Email is required![/red]")
                    user_email = None
                    continue

                # Check if user exists
                result = await db.execute(select(User).where(User.email == user_email))
                existing_user = result.scalar_one_or_none()

                if existing_user:
                    console.print(
                        f"[red]❌ User with email '{user_email}' already exists![/red]"
                    )
                    if email:  # If email was provided via option, abort
                        raise typer.Exit(1)
                    retry = Confirm.ask("Try another email?", default=True)
                    if not retry:
                        raise typer.Abort()
                    user_email = None
                    continue
                break

            # Get name
            user_name = name
            if not user_name:
                user_name = Prompt.ask(
                    "[bold]Full name[/bold]", default="Admin User"
                ).strip()

            # Get phone
            user_phone = phone
            if not user_phone:
                user_phone = Prompt.ask(
                    "[bold]Phone number[/bold] (optional)", default=""
                ).strip()

            # Get password
            while True:
                password = getpass("Password: ").strip()
                if not password:
                    console.print("[red]❌ Password is required![/red]")
                    continue

                if len(password) < 6:
                    console.print(
                        "[red]❌ Password must be at least 6 characters![/red]"
                    )
                    continue

                password_confirm = getpass("Password (again): ").strip()
                if password != password_confirm:
                    console.print("[red]❌ Passwords don't match![/red]")
                    continue
                break

            # Create superuser
            admin = User(
                name=user_name,
                email=user_email,
                phone=user_phone if user_phone else None,
                password_hash=get_password_hash(password),
                role="admin",
            )
            db.add(admin)
            await db.commit()

            console.print()
            console.print(
                Panel(
                    f"[bold green]✅ Superuser created successfully![/bold green]\n\n"
                    f"[cyan]Email:[/cyan] {user_email}\n"
                    f"[cyan]Name:[/cyan] {user_name}\n"
                    f"[cyan]Role:[/cyan] admin",
                    title="Success",
                    border_style="green",
                )
            )
            console.print()

    asyncio.run(run())


@app.command("create-tables")
def create_database_tables():
    """
    Create all database tables without seeding data.

    Useful for initial database setup.
    """
    console.print("\n[bold cyan]📋 Creating database tables...[/bold cyan]\n")

    async def run():
        await create_tables()

    asyncio.run(run())
    console.print("\n[bold green]✅ Tables created successfully![/bold green]\n")


@app.command("list")
def list_tables():
    """
    List all available tables that can be seeded.
    """
    console.print()
    table = Table(title="Available Tables", show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Table Name", style="cyan")
    table.add_column("Description", style="white")

    descriptions = {
        "users": "Admin and client users with authentication",
        "packages": "Event packages with pricing and items",
        "gallery": "Gallery items with images and categories",
        "contact_info": "Business contact information",
        "contact_messages": "Sample contact form submissions",
        "themes": "Event themes with gallery images",
        "testimonials": "Customer testimonials and reviews",
        "bookings": "Sample event bookings",
        "translations": "Multilingual content translations",
    }

    for idx, table_name in enumerate(TableName, 1):
        table.add_row(
            str(idx), table_name.value, descriptions.get(table_name.value, "")
        )

    console.print(table)
    console.print()


@app.command("info")
def show_info():
    """
    Show information about default credentials and sample data.
    """
    console.print()
    console.print(
        Panel(
            "[bold cyan]Default User Credentials[/bold cyan]\n\n"
            "[yellow]Admin Account:[/yellow]\n"
            "  Email: admin@lushmoments.com\n"
            "  Password: Admin@123\n\n"
            "[yellow]Client Account:[/yellow]\n"
            "  Email: client@example.com\n"
            "  Password: Client@123\n\n"
            "[dim]These accounts are created when seeding the 'users' table.[/dim]",
            title="🔐 Authentication",
            border_style="cyan",
        )
    )
    console.print()
    console.print(
        Panel(
            "[bold cyan]Sample Data Overview[/bold cyan]\n\n"
            "• [yellow]4 Packages[/yellow]: Starter, Classic, Premium, Ultimate\n"
            "• [yellow]5 Gallery Items[/yellow]: Wedding, corporate, birthday events\n"
            "• [yellow]6 Themes[/yellow]: Romantic, modern, rustic, etc.\n"
            "• [yellow]5 Testimonials[/yellow]: Customer reviews\n"
            "• [yellow]3 Bookings[/yellow]: Sample event bookings\n"
            "• [yellow]6 Translations[/yellow]: Spanish and French samples",
            title="📊 Data Summary",
            border_style="green",
        )
    )
    console.print()


if __name__ == "__main__":
    app()
