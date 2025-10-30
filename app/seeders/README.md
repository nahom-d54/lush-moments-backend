# Database Seeders

A modular, pluggable seeder system for Lush Moments Backend.

## Overview

The seeder system follows a registry pattern where each seeder is:
- **Independent**: Can be run individually without modifying other seeders
- **Pluggable**: New seeders auto-register themselves when created
- **Idempotent**: Safe to run multiple times without creating duplicates
- **Dependency-aware**: Can specify dependencies on other seeders

## Directory Structure

```
app/seeders/
├── __init__.py              # Package initialization with auto-imports
├── base.py                  # BaseSeeder abstract class
├── registry.py              # SeederRegistry for managing seeders
├── user_seeder.py           # User accounts seeder
├── package_seeder.py        # Event packages seeder
├── faq_seeder.py            # FAQs seeder
├── enhancement_seeder.py    # Package enhancements seeder
├── theme_seeder.py          # Event themes seeder
├── gallery_seeder.py        # Gallery items seeder
├── testimonial_seeder.py    # Customer testimonials seeder
└── contact_info_seeder.py   # Business contact info seeder
```

## Usage

### Run All Seeders

```bash
python seed.py
```

### Run Specific Seeders

```bash
python seed.py users packages faqs
```

### List Available Seeders

```bash
python seed.py --list
```

## Creating a New Seeder

1. **Create a new file** in `app/seeders/` (e.g., `my_seeder.py`)

2. **Implement the seeder class**:

```python
"""
My Custom Seeder

Description of what this seeder does.
"""

from sqlalchemy import select
from app.models import MyModel
from .base import BaseSeeder
from .registry import registry


class MyCustomSeeder(BaseSeeder):
    """Seed my custom data"""

    name = "my_custom"
    description = "Create my custom data"
    dependencies = []  # List of seeder names that must run first

    async def should_run(self) -> bool:
        """Check if data already exists"""
        result = await self.db.execute(select(MyModel))
        return result.scalar_one_or_none() is None

    async def run(self) -> None:
        """Create the data"""
        # Your seeding logic here
        items = [
            MyModel(field1="value1"),
            MyModel(field2="value2"),
        ]
        self.db.add_all(items)
        await self.db.commit()
        print(f"  - Created {len(items)} items")


# Auto-register this seeder
registry.register(MyCustomSeeder)
```

3. **Import the seeder** in `app/seeders/__init__.py`:

```python
from .my_seeder import MyCustomSeeder

__all__ = [
    # ... existing seeders ...
    "MyCustomSeeder",
]
```

4. **Import in seed.py** (for auto-registration):

```python
from app.seeders.my_seeder import MyCustomSeeder  # noqa: F401
```

That's it! Your seeder is now pluggable and available.

## Seeder Features

### Dependencies

Seeders can depend on other seeders:

```python
class BookingSeeder(BaseSeeder):
    name = "bookings"
    dependencies = ["users", "packages"]  # Runs after users and packages
```

### Conditional Running

Override `should_run()` to control when a seeder executes:

```python
async def should_run(self) -> bool:
    """Only run if no data exists"""
    result = await self.db.execute(select(MyModel))
    return result.scalar_one_or_none() is None
```

### Progress Feedback

Use print statements to show progress:

```python
async def run(self) -> None:
    items = create_items()
    self.db.add_all(items)
    await self.db.commit()
    print(f"  - Created {len(items)} items")
    print(f"  - Admin: admin@example.com / Admin@123")
```

## Available Seeders

| Name | Description | Dependencies |
|------|-------------|--------------|
| `users` | Create admin and sample client users | None |
| `packages` | Create event packages with items | None |
| `faqs` | Create frequently asked questions | None |
| `enhancements` | Create package add-ons and enhancements | None |
| `themes` | Create event themes | None |
| `gallery` | Create gallery items | None |
| `testimonials` | Create customer testimonials | None |
| `contact_info` | Create business contact information | None |

## Best Practices

1. **Keep seeders independent**: Don't modify existing seeders when adding new ones
2. **Make seeders idempotent**: Check if data exists before creating
3. **Use clear names**: Seeder names should be descriptive
4. **Document your seeder**: Add a module docstring explaining what it does
5. **Handle dependencies**: Use the `dependencies` list if your seeder needs others to run first
6. **Provide feedback**: Print meaningful progress messages

## Example Usage

```bash
# First time setup - seed everything
python seed.py

# Add only FAQs and enhancements
python seed.py faqs enhancements

# Check what seeders are available
python seed.py --list

# Seed with virtual environment
.venv/Scripts/python.exe seed.py
```

## Troubleshooting

### "Seeder not found" error

Make sure:
1. The seeder is imported in `app/seeders/__init__.py`
2. The seeder calls `registry.register(YourSeederClass)` at the bottom
3. The seeder is imported in `seed.py` (with `# noqa: F401`)

### "Already exists" warnings

This is normal! Seeders check if data exists and skip re-creating it. This makes them safe to run multiple times.

### Dependency errors

If you see dependency errors, check:
1. The dependency seeder names are spelled correctly
2. The dependent seeders are registered before running
3. No circular dependencies exist

## Architecture

```
seed.py (CLI)
    ↓
SeederRegistry (Manages all seeders)
    ↓
BaseSeeder (Abstract class)
    ↓
[Individual Seeders] (Concrete implementations)
```

The system uses:
- **Registry Pattern**: Central registration of all seeders
- **Template Method**: BaseSeeder defines the structure
- **Dependency Resolution**: Automatic ordering based on dependencies
- **Idempotent Operations**: Safe to run multiple times
