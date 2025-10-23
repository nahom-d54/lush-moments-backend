# Lush Moments CLI Documentation

Command-line interface for managing the Lush Moments backend application.

## Installation

The CLI is automatically available when you install the project dependencies:

```bash
uv sync
```

## Usage

Run the CLI with:

```bash
uv run python cli.py [COMMAND] [OPTIONS]
```

Or if you have the package installed with entry points:

```bash
lush-cli [COMMAND] [OPTIONS]
```

## Commands

### `create-admin`

Create a new admin user (super admin).

**Usage:**
```bash
uv run python cli.py create-admin [OPTIONS]
```

**Options:**
- `--email, -e TEXT`: Admin email address
- `--name, -n TEXT`: Admin full name
- `--password, -p TEXT`: Admin password
- `--phone TEXT`: Admin phone number (optional)

**Examples:**

Interactive mode (prompts for all values):
```bash
uv run python cli.py create-admin
```

With all options:
```bash
uv run python cli.py create-admin \
  --email "admin@lushmoments.com" \
  --name "Admin User" \
  --password "SecurePassword123" \
  --phone "+1234567890"
```

With some options (prompts for missing values):
```bash
uv run python cli.py create-admin --email "admin@lushmoments.com"
```

---

### `list-admins`

List all admin users in the system.

**Usage:**
```bash
uv run python cli.py list-admins
```

**Output:**
Displays a table with admin user details:
- ID
- Name
- Email
- Phone

**Example:**
```bash
uv run python cli.py list-admins
```

---

### `list-users`

List all users in the system.

**Usage:**
```bash
uv run python cli.py list-users [OPTIONS]
```

**Options:**
- `--role, -r TEXT`: Filter by role (admin/client)

**Examples:**

List all users:
```bash
uv run python cli.py list-users
```

List only admin users:
```bash
uv run python cli.py list-users --role admin
```

List only client users:
```bash
uv run python cli.py list-users --role client
```

---

### `change-password`

Change password for a user account.

**Usage:**
```bash
uv run python cli.py change-password [OPTIONS]
```

**Options:**
- `--email, -e TEXT`: User email address

**Example:**

Interactive mode:
```bash
uv run python cli.py change-password
# You'll be prompted for:
# - Email address
# - New password
# - Password confirmation
```

With email option:
```bash
uv run python cli.py change-password --email "user@example.com"
# You'll be prompted for:
# - New password
# - Password confirmation
```

---

### `delete-user`

Delete a user account from the system.

**Usage:**
```bash
uv run python cli.py delete-user [OPTIONS]
```

**Options:**
- `--email, -e TEXT`: User email address
- `--force, -f`: Skip confirmation prompt

**Examples:**

Interactive mode (with confirmation):
```bash
uv run python cli.py delete-user --email "user@example.com"
# You'll be prompted to confirm the deletion
```

Skip confirmation:
```bash
uv run python cli.py delete-user --email "user@example.com" --force
```

---

### `init-db`

Initialize the database by creating all tables.

**Usage:**
```bash
uv run python cli.py init-db
```

**Description:**
Creates all database tables according to the defined models. This command is idempotent - it won't recreate tables that already exist.

**Example:**
```bash
uv run python cli.py init-db
```

---

### `seed-db`

Seed the database with initial data for development and testing.

**Usage:**
```bash
uv run python cli.py seed-db [OPTIONS]
```

**Options:**
- `--clear, -c`: Clear existing data before seeding (destructive!)

**Description:**
Populates the database with sample data including:
- Admin and client users
- Event packages (4 packages)
- Themes (6 themes)
- Testimonials (5 testimonials)
- Sample translations (Spanish and French)
- Sample bookings (3 bookings)

**Examples:**

Seed database (skip if data already exists):
```bash
uv run python cli.py seed-db
```

Clear and reseed database:
```bash
uv run python cli.py seed-db --clear
# You'll be prompted to confirm data deletion
```

**Seeded Data:**

Users:
- Admin: `admin@lushmoments.com` / `Admin@123`
- Client: `client@example.com` / `Client@123`

Packages:
- Starter Package ($500)
- Classic Package ($1,200)
- Premium Package ($2,500)
- Ultimate Package ($5,000)

Themes:
- Romantic Garden
- Modern Minimalist
- Rustic Charm
- Classic Elegance
- Tropical Paradise
- Corporate Professional

---

### `version`

Display version information about the application.

**Usage:**
```bash
uv run python cli.py version
```

**Output:**
- Application name
- Version number
- Framework
- Database technology

**Example:**
```bash
uv run python cli.py version
```

---

## Common Workflows

### Initial Setup

1. Initialize database:
```bash
uv run python cli.py init-db
```

2. Seed with sample data:
```bash
uv run python cli.py seed-db
```

3. Create your super admin:
```bash
uv run python cli.py create-admin \
  --email "youremail@lushmoments.com" \
  --name "Your Name" \
  --password "YourSecurePassword"
```

### Production Deployment

1. Initialize database:
```bash
uv run python cli.py init-db
```

2. Create production admin (no sample data):
```bash
uv run python cli.py create-admin \
  --email "admin@yourdomain.com" \
  --name "Production Admin" \
  --password "StrongProductionPassword"
```

### User Management

List all admins:
```bash
uv run python cli.py list-admins
```

Create additional admin:
```bash
uv run python cli.py create-admin
```

Change user password:
```bash
uv run python cli.py change-password --email "user@example.com"
```

Remove user:
```bash
uv run python cli.py delete-user --email "user@example.com"
```

### Development Reset

Clear and reseed database for fresh start:
```bash
uv run python cli.py seed-db --clear
```

## Security Notes

1. **Passwords**: Always use strong passwords in production
2. **Admin Creation**: Protect admin creation commands in production
3. **Force Deletion**: Use `--force` flag carefully to avoid accidental deletions
4. **Database Clear**: The `--clear` flag is destructive - use with extreme caution

## Troubleshooting

### Database Connection Issues

If you see database connection errors:
1. Check your `.env` file for correct `DATABASE_URL`
2. Ensure database server is running
3. Verify database credentials

### Permission Issues

If you get permission errors:
1. Check file permissions on database file (SQLite)
2. Ensure user running the command has proper permissions
3. Check database server permissions (PostgreSQL)

### Import Errors

If you see import errors:
1. Ensure all dependencies are installed: `uv sync`
2. Check Python version compatibility (requires Python 3.12+)
3. Verify virtual environment is activated

## Help

Get help for any command:
```bash
uv run python cli.py --help
uv run python cli.py [COMMAND] --help
```

Example:
```bash
uv run python cli.py create-admin --help
```