# Database Seeder Guide

A Django-style interactive database seeding utility for Lush Moments backend.

## Quick Start

### Interactive Mode (Recommended)
```bash
python seed.py
```

This opens an interactive menu with options:
1. Seed all tables
2. Fresh seed (drop all & reseed)
3. Seed specific table
4. Drop all tables
5. **Create superuser** (like Django's createsuperuser)
6. Create tables only
0. Exit

### Command Line Usage

#### Create Superuser
```bash
python seed.py --superuser
```

Interactively creates an admin user with:
- Email validation (checks for duplicates)
- Password confirmation
- Optional phone number

#### Seed All Tables
```bash
python seed.py --all
```

Seeds all tables with sample data:
- Users (admin + sample client)
- Packages (4 pricing tiers with items)
- Gallery (5 sample images with categories)
- Contact Info (business details)
- Contact Messages (2 sample inquiries)
- Themes (6 event themes)
- Testimonials (5 customer reviews)
- Bookings (3 sample bookings)
- Translations (sample multilingual content)

#### Fresh Seed (Drop & Reseed)
```bash
python seed.py --fresh
```

⚠️ **WARNING**: This drops all tables and recreates them with fresh data. All existing data will be lost!

#### Seed Specific Table
```bash
python seed.py --table users
python seed.py --table packages
python seed.py --table themes
```

Available tables:
- `users` - Admin and client users
- `packages` - Event packages
- `gallery` - Gallery items
- `contact_info` - Business contact information
- `contact_messages` - Sample contact form submissions
- `themes` - Event themes
- `testimonials` - Customer testimonials
- `bookings` - Sample event bookings
- `translations` - Multilingual translations

#### Drop All Tables
```bash
python seed.py --drop
```

⚠️ **WARNING**: Requires confirmation. Drops all tables and data.

#### Help
```bash
python seed.py --help
```

## Default Credentials

After seeding users, you can login with:

**Admin Account:**
- Email: `admin@lushmoments.com`
- Password: `Admin@123`

**Client Account:**
- Email: `client@example.com`
- Password: `Client@123`

## Common Workflows

### First Time Setup
```bash
# Interactive mode - choose option 1 (Seed all tables)
python seed.py
```

### Create Custom Admin
```bash
# Create your own admin account
python seed.py --superuser
```

### Reset Database
```bash
# Drop everything and reseed
python seed.py --fresh
```

### Development Testing
```bash
# Reseed specific table after making changes
python seed.py --table themes
```

## Features

### ✅ Interactive Menu
- User-friendly interface
- No need to remember commands
- Confirmation prompts for destructive actions

### ✅ Create Superuser
- Email validation with duplicate checking
- Password strength validation (min 6 characters)
- Password confirmation
- Optional fields (phone)

### ✅ Selective Seeding
- Seed individual tables
- Skip tables that already have data
- Helpful skip messages

### ✅ Safety Features
- Confirmation required for drop operations
- Clear warning messages
- Keyboard interrupt handling (Ctrl+C)

### ✅ Django-like Experience
- Familiar command structure
- Interactive prompts
- Clear success/error messages

## Examples

### Example 1: First Time Setup
```bash
$ python seed.py

==================================================
LUSH MOMENTS DATABASE SEEDER
==================================================

1. Seed all tables
2. Fresh seed (drop all & reseed)
3. Seed specific table
4. Drop all tables
5. Create superuser
6. Create tables only
0. Exit

--------------------------------------------------

Select an option (0-6): 1

🌱 Seeding all tables...
✓ Database tables created
✓ Users seeded successfully
  - Admin: admin@lushmoments.com / Admin@123
  - Client: client@example.com / Client@123
✓ 4 packages with items seeded successfully
✓ 5 gallery items seeded successfully
...
```

### Example 2: Create Custom Admin
```bash
$ python seed.py --superuser

==================================================
CREATE SUPERUSER
==================================================

Email address: john@lushmoments.com
Full name: John Doe
Phone number (optional): +1-555-1234
Password: 
Password (again): 

✅ Superuser 'john@lushmoments.com' created successfully!
==================================================
```

### Example 3: Reset Specific Table
```bash
$ python seed.py

Select an option (0-6): 3

Available tables:
1. users
2. packages
3. gallery
4. contact_info
5. contact_messages
6. themes
7. testimonials
8. bookings
9. translations

Enter table name: themes

🌱 Seeding themes...
⚠ Themes already exist, skipping...
✅ themes seeded successfully!
```

## Troubleshooting

### "Module not found" error
Make sure you're using the virtual environment Python:
```bash
.\.venv\Scripts\python.exe seed.py
```

Or activate the environment first:
```bash
# PowerShell (if allowed)
.\.venv\Scripts\Activate.ps1
python seed.py

# Or use full path
.\.venv\Scripts\python.exe seed.py
```

### "Table already exists" warnings
These are normal! The seeder checks for existing data and skips tables that are already populated. Use `--fresh` to drop and reseed.

### Database locked error
Make sure the FastAPI server is stopped before running destructive operations:
```bash
# Stop the server (Ctrl+C in the terminal running uvicorn)
# Then run seeder
python seed.py --fresh
```

## Notes

- All seeders check for existing data before inserting
- Gallery images and theme images reference placeholder paths (create actual images separately)
- Translations are sample data for Spanish and French
- Sample bookings have realistic dates (30-90 days in the future)
- All passwords are hashed using bcrypt

## Related Files

- `seed.py` - Main interactive CLI script
- `app/seeders/seed_new.py` - Individual seeder functions
- `app/seeders/seed.py` - Alternative seeder (legacy)
- `app/models/` - Database models
- `app/utils/auth.py` - Password hashing utilities
