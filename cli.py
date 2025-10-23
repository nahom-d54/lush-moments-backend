"""
Lush Moments Backend CLI

Command-line interface for managing the backend application.
"""

import asyncio

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table
from sqlalchemy import select

from app.database import AsyncSessionLocal, Base, engine
from app.models import User
from app.utils.auth import get_password_hash

app = typer.Typer(
    name="lush-moments",
    help="Lush Moments Backend Management CLI",
    add_completion=False,
)
console = Console()


@app.command()
def create_admin(
    email: str = typer.Option(None, "--email", "-e", help="Admin email address"),
    name: str = typer.Option(None, "--name", "-n", help="Admin full name"),
    password: str = typer.Option(None, "--password", "-p", help="Admin password"),
    phone: str = typer.Option(None, "--phone", help="Admin phone number (optional)"),
):
    """
    Create a new admin user (super admin)
    """
    console.print("\n[bold cyan]Create Super Admin User[/bold cyan]\n")

    # Interactive prompts if values not provided
    if not email:
        email = Prompt.ask("Enter email address")

    if not name:
        name = Prompt.ask("Enter full name")

    if not password:
        password = Prompt.ask("Enter password", password=True)
        password_confirm = Prompt.ask("Confirm password", password=True)

        if password != password_confirm:
            console.print("[bold red]✗ Passwords do not match![/bold red]")
            raise typer.Exit(1)

    if not phone:
        phone = Prompt.ask(
            "Enter phone number (optional, press Enter to skip)", default=""
        )
        if phone == "":
            phone = None

    async def _create_admin():
        async with AsyncSessionLocal() as db:
            # Check if email already exists
            result = await db.execute(select(User).where(User.email == email))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                console.print(
                    f"[bold red]✗ User with email {email} already exists![/bold red]"
                )
                return False

            # Create admin user
            admin = User(
                name=name,
                email=email,
                phone=phone,
                password_hash=get_password_hash(password),
                role="admin",
            )
            db.add(admin)
            await db.commit()
            await db.refresh(admin)

            console.print(
                "\n[bold green]✓ Admin user created successfully![/bold green]"
            )
            console.print(f"  ID: {admin.id}")
            console.print(f"  Name: {admin.name}")
            console.print(f"  Email: {admin.email}")
            console.print(f"  Role: {admin.role}")
            if admin.phone:
                console.print(f"  Phone: {admin.phone}")
            return True

    success = asyncio.run(_create_admin())
    if not success:
        raise typer.Exit(1)


@app.command()
def list_admins():
    """
    List all admin users
    """

    async def _list_admins():
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User).where(User.role == "admin"))
            admins = result.scalars().all()

            if not admins:
                console.print("[yellow]No admin users found.[/yellow]")
                return

            table = Table(title="Admin Users")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Email", style="blue")
            table.add_column("Phone", style="magenta")

            for admin in admins:
                table.add_row(
                    str(admin.id),
                    admin.name,
                    admin.email,
                    admin.phone or "N/A",
                )

            console.print(table)

    asyncio.run(_list_admins())


@app.command()
def change_password(
    email: str = typer.Option(None, "--email", "-e", help="User email address"),
):
    """
    Change password for a user
    """
    console.print("\n[bold cyan]Change User Password[/bold cyan]\n")

    if not email:
        email = Prompt.ask("Enter user email address")

    new_password = Prompt.ask("Enter new password", password=True)
    password_confirm = Prompt.ask("Confirm new password", password=True)

    if new_password != password_confirm:
        console.print("[bold red]✗ Passwords do not match![/bold red]")
        raise typer.Exit(1)

    async def _change_password():
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

            if not user:
                console.print(
                    f"[bold red]✗ User with email {email} not found![/bold red]"
                )
                return False

            user.password_hash = get_password_hash(new_password)
            await db.commit()

            console.print(
                f"\n[bold green]✓ Password changed successfully for {user.name}![/bold green]"
            )
            return True

    success = asyncio.run(_change_password())
    if not success:
        raise typer.Exit(1)


@app.command()
def delete_user(
    email: str = typer.Option(None, "--email", "-e", help="User email address"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation prompt"),
):
    """
    Delete a user account
    """
    if not email:
        email = Prompt.ask("Enter user email address")

    if not force:
        confirm = Confirm.ask(f"Are you sure you want to delete user {email}?")
        if not confirm:
            console.print("[yellow]Operation cancelled.[/yellow]")
            raise typer.Exit(0)

    async def _delete_user():
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()

            if not user:
                console.print(
                    f"[bold red]✗ User with email {email} not found![/bold red]"
                )
                return False

            await db.delete(user)
            await db.commit()

            console.print(
                f"\n[bold green]✓ User {user.name} deleted successfully![/bold green]"
            )
            return True

    success = asyncio.run(_delete_user())
    if not success:
        raise typer.Exit(1)


@app.command()
def init_db():
    """
    Initialize database (create all tables)
    """

    async def _init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        console.print("[bold green]✓ Database initialized successfully![/bold green]")

    asyncio.run(_init_db())


@app.command()
def seed_db(
    clear: bool = typer.Option(
        False, "--clear", "-c", help="Clear existing data before seeding"
    ),
):
    """
    Seed database with initial data
    """
    if clear:
        confirm = Confirm.ask("This will delete all existing data. Are you sure?")
        if not confirm:
            console.print("[yellow]Operation cancelled.[/yellow]")
            raise typer.Exit(0)

    # Import here to avoid circular imports
    from app.seeders.seed import clear_tables, seed_all

    async def _seed():
        if clear:
            await clear_tables()
        await seed_all()

    asyncio.run(_seed())


@app.command()
def list_users(
    role: str = typer.Option(
        None, "--role", "-r", help="Filter by role (admin/client)"
    ),
):
    """
    List all users
    """

    async def _list_users():
        async with AsyncSessionLocal() as db:
            query = select(User)
            if role:
                query = query.where(User.role == role)

            result = await db.execute(query)
            users = result.scalars().all()

            if not users:
                console.print(
                    f"[yellow]No {role + ' ' if role else ''}users found.[/yellow]"
                )
                return

            table = Table(title=f"{role.title() + ' ' if role else ''}Users")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Email", style="blue")
            table.add_column("Role", style="yellow")
            table.add_column("Phone", style="magenta")

            for user in users:
                table.add_row(
                    str(user.id),
                    user.name,
                    user.email,
                    user.role if isinstance(user.role, str) else user.role.value,
                    user.phone or "N/A",
                )

            console.print(table)

    asyncio.run(_list_users())


@app.command()
def version():
    """
    Show version information
    """
    console.print("\n[bold cyan]Lush Moments Backend[/bold cyan]")
    console.print("Version: 0.1.0")
    console.print("Framework: FastAPI")
    console.print("Database: SQLAlchemy + AsyncIO\n")


if __name__ == "__main__":
    app()
