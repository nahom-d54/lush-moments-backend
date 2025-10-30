"""
Base Seeder Class

Provides the foundation for all database seeders.
"""

from abc import ABC, abstractmethod
from typing import ClassVar

from sqlalchemy.ext.asyncio import AsyncSession


class BaseSeeder(ABC):
    """
    Abstract base class for all seeders.

    Each seeder must implement:
    - name: Unique identifier for the seeder
    - description: Human-readable description
    - run(): Method to execute the seeding logic
    """

    name: ClassVar[str] = ""
    description: ClassVar[str] = ""
    dependencies: ClassVar[list[str]] = []  # Names of seeders that must run first

    def __init__(self, db: AsyncSession):
        """
        Initialize the seeder with a database session.

        Args:
            db: SQLAlchemy async session
        """
        self.db = db

    @abstractmethod
    async def run(self) -> None:
        """
        Execute the seeding logic.

        This method should be idempotent - running it multiple times
        should not create duplicate data.
        """
        pass

    async def should_run(self) -> bool:
        """
        Determine if this seeder should run.

        Override this method to add custom logic for checking
        if the seeder needs to run (e.g., check if data already exists).

        Returns:
            bool: True if seeder should run, False otherwise
        """
        return True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"
