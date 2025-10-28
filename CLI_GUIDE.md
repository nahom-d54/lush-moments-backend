# Lush Moments Management CLI

A powerful Django-style management interface for database operations using **Typer** and **Rich**.

## 🚀 Quick Start

```bash
# Show all available commands
python manage.py --help

# See information about default credentials
python manage.py info

# List all available tables
python manage.py list

# Seed all tables
python manage.py all

# Create an admin user
python manage.py createsuperuser
```

## 📋 Available Commands

### `all` - Seed All Tables
Seeds all database tables with comprehensive sample data.

```bash
python manage.py all
```

**What it seeds:**
- ✅ 2 Users (admin + client with default passwords)
- ✅ 4 Packages (Starter, Classic, Premium, Ultimate)
- ✅ 5 Gallery Items (various event categories)
- ✅ Business Contact Information
- ✅ 2 Sample Contact Messages
- ✅ 6 Event Themes
- ✅ 5 Customer Testimonials
- ✅ 3 Sample Bookings
- ✅ 6 Translations (Spanish & French)

### `fresh` - Fresh Seed (Destructive)
Drops all tables and reseeds with fresh data.

```bash
# Interactive mode (asks for confirmation)
python manage.py fresh

# Force mode (skips confirmation)
python manage.py fresh --force
```

⚠️ **WARNING**: This command will **DELETE ALL DATA** from your database!

### `table` - Seed Specific Table
Seeds a single table with sample data.

```bash
python manage.py table users
python manage.py table packages
python manage.py table themes
python manage.py table testimonials
```

**Available tables:**
- `users` - Admin and client users
- `packages` - Event packages
- `gallery` - Gallery items
- `contact_info` - Business contact info
- `contact_messages` - Contact form messages
- `themes` - Event themes
- `testimonials` - Customer testimonials
- `bookings` - Event bookings
- `translations` - Multilingual content

### `drop` - Drop All Tables (Destructive)
Drops all database tables.

```bash
# Interactive mode (asks for confirmation)
python manage.py drop

# Force mode (skips confirmation)
python manage.py drop --force
```

⚠️ **WARNING**: This command will **DELETE ALL DATA** from your database!

### `createsuperuser` - Create Admin User
Interactively creates an admin user account.

```bash
# Interactive mode
python manage.py createsuperuser

# With options
python manage.py createsuperuser --email admin@test.com --name "Admin"
```

**Features:**
- ✅ Email validation with duplicate checking
- ✅ Password confirmation
- ✅ Password strength validation (minimum 6 characters)
- ✅ Optional phone number
- ✅ Automatic password hashing

**Options:**
- `--email` / `-e` - Admin email address
- `--name` / `-n` - Admin full name
- `--phone` / `-p` - Phone number (optional)

**Example:**
```bash
$ python manage.py createsuperuser

╭─ 🔐 Create Superuser ─╮
│ Create a new admin user│
╰────────────────────────╯

Email address: john@lushmoments.com
Full name [Admin User]: John Doe
Phone number (optional): +1-555-1234
Password: 
Password (again): 

╭─ Success ─────────────────────╮
│ ✅ Superuser created successfully! │
│                                │
│ Email: john@lushmoments.com    │
│ Name: John Doe                 │
│ Role: admin                    │
╰────────────────────────────────╯
```

### `create-tables` - Create Tables Only
Creates all database tables without seeding data.

```bash
python manage.py create-tables
```

Useful for:
- Initial database setup
- After migrations
- Testing empty database state

### `list` - List Available Tables
Shows all tables that can be seeded with descriptions.

```bash
python manage.py list
```

**Output:**
```
                Available Tables                
┏━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ #  ┃ Table Name      ┃ Description                ┃
┡━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ users           │ Admin and client users...  │
│ 2  │ packages        │ Event packages...          │
│ 3  │ gallery         │ Gallery items...           │
└────┴─────────────────┴────────────────────────────┘
```

### `info` - Show Default Credentials
Displays default credentials and sample data overview.

```bash
python manage.py info
```

**Output:**
- Default admin credentials
- Default client credentials
- Summary of sample data

## 🔐 Default Credentials

After seeding users, you can login with:

### Admin Account
```
Email: admin@lushmoments.com
Password: Admin@123
```

### Client Account
```
Email: client@example.com
Password: Client@123
```

## 📚 Common Workflows

### First Time Setup
```bash
# 1. Create database tables and seed all data
python manage.py all

# 2. Check the default credentials
python manage.py info

# 3. Start the server and login
uvicorn app.main:app --reload
```

### Create Custom Admin
```bash
# Create your own admin account
python manage.py createsuperuser
```

### Development Testing
```bash
# Reset database with fresh data
python manage.py fresh --force

# Reseed specific table after testing
python manage.py table themes
```

### Production Setup
```bash
# 1. Create tables only (no sample data)
python manage.py create-tables

# 2. Create admin user
python manage.py createsuperuser --email admin@yourcompany.com
```

## 🎨 Features

### ✅ Beautiful Terminal UI
- Powered by [Rich](https://rich.readthedocs.io/) for gorgeous terminal output
- Color-coded messages (success, warning, error)
- Styled tables and panels
- Progress indicators

### ✅ Type Safety
- Built with [Typer](https://typer.tiangolo.com/) for robust CLI
- Enum-based table names (autocomplete support)
- Type hints throughout

### ✅ Safety Features
- Confirmation prompts for destructive operations
- `--force` flag to skip confirmations (for scripts)
- Clear warning messages
- Duplicate email checking
- Password validation

### ✅ Django-like Experience
- Familiar command structure
- Interactive prompts
- `createsuperuser` command
- `fresh` command for development

## 🔧 Advanced Usage

### Running with Virtual Environment
```bash
# Activate virtual environment first
.\.venv\Scripts\Activate.ps1
python manage.py all

# Or use full path (Windows)
.\.venv\Scripts\python.exe manage.py all

# Or use full path (Linux/Mac)
./venv/bin/python manage.py all
```

### Scripting / Automation
```bash
# Use --force to skip confirmations
python manage.py fresh --force

# Combine with other commands
python manage.py fresh --force && python manage.py createsuperuser --email admin@test.com --name Admin
```

### Help for Specific Commands
```bash
# Get help for any command
python manage.py createsuperuser --help
python manage.py fresh --help
python manage.py table --help
```

## 🐛 Troubleshooting

### Command Not Found
Make sure you're using the correct Python:
```bash
# Windows
.\.venv\Scripts\python.exe manage.py --help

# Linux/Mac
./venv/bin/python manage.py --help
```

### Module Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
# or
uv pip install -e .
```

### Database Locked
Stop the FastAPI server before running destructive operations:
```bash
# Stop uvicorn (Ctrl+C)
# Then run:
python manage.py fresh --force
```

### "Table already exists" Warnings
These are normal! The seeder checks for existing data and skips tables that are already populated. Use `fresh` to drop and reseed:
```bash
python manage.py fresh
```

## 📁 File Structure

```
lush-moments-backend/
├── manage.py                  # Main CLI entry point
├── app/
│   └── seeders/
│       ├── cli.py            # Typer CLI implementation
│       ├── seed_new.py       # Seeder functions
│       └── seed.py           # Legacy seeder
└── SEEDER_GUIDE.md           # This file
```

## 🔗 Related Documentation

- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

## 💡 Tips

1. **Always backup production data** before running destructive commands
2. Use `--force` flag in CI/CD pipelines to avoid interactive prompts
3. Run `python manage.py info` to quickly check default credentials
4. Use `python manage.py list` to see all available tables
5. Create custom admin users with `createsuperuser` instead of using defaults

## 📝 Examples

### Scenario 1: Setting up development environment
```bash
# Clone repo, install deps, then:
python manage.py fresh --force
python manage.py info
# Start coding!
```

### Scenario 2: Testing a new feature
```bash
# Reset specific table
python manage.py table bookings

# Or reset everything
python manage.py fresh --force
```

### Scenario 3: Production deployment
```bash
# Don't seed sample data in production!
python manage.py create-tables
python manage.py createsuperuser
```

---

**Made with ❤️ using Typer and Rich**
