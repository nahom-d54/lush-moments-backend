"""
Seeder Registry

Manages registration and execution of all seeders.
"""

from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseSeeder


class SeederRegistry:
    """
    Registry for managing and executing seeders.

    Seeders are automatically discovered and can be run individually
    or in a specific order based on dependencies.
    """

    def __init__(self):
        self._seeders: dict[str, Type[BaseSeeder]] = {}

    def register(self, seeder_class: Type[BaseSeeder]) -> None:
        """
        Register a seeder class.

        Args:
            seeder_class: The seeder class to register
        """
        if not seeder_class.name:
            raise ValueError(
                f"Seeder {seeder_class.__name__} must have a 'name' attribute"
            )

        if seeder_class.name in self._seeders:
            raise ValueError(
                f"Seeder with name '{seeder_class.name}' is already registered"
            )

        self._seeders[seeder_class.name] = seeder_class

    def get_seeder(self, name: str) -> Type[BaseSeeder] | None:
        """Get a seeder class by name."""
        return self._seeders.get(name)

    def list_seeders(self) -> list[tuple[str, str]]:
        """
        List all registered seeders.

        Returns:
            List of (name, description) tuples
        """
        return [(name, cls.description) for name, cls in self._seeders.items()]

    def _resolve_dependencies(self, seeder_names: list[str]) -> list[str]:
        """
        Resolve seeder dependencies and return execution order.

        Args:
            seeder_names: List of seeder names to execute

        Returns:
            Ordered list of seeder names based on dependencies
        """
        executed = set()
        execution_order = []

        def resolve(name: str):
            if name in executed:
                return

            seeder_class = self._seeders.get(name)
            if not seeder_class:
                raise ValueError(f"Seeder '{name}' not found")

            # Resolve dependencies first
            for dep in seeder_class.dependencies:
                if dep not in self._seeders:
                    raise ValueError(
                        f"Dependency '{dep}' for seeder '{name}' not found"
                    )
                resolve(dep)

            execution_order.append(name)
            executed.add(name)

        for name in seeder_names:
            resolve(name)

        return execution_order

    async def run_seeder(self, name: str, db: AsyncSession) -> bool:
        """
        Run a single seeder.

        Args:
            name: Name of the seeder to run
            db: Database session

        Returns:
            bool: True if seeder ran, False if skipped
        """
        seeder_class = self._seeders.get(name)
        if not seeder_class:
            raise ValueError(f"Seeder '{name}' not found")

        seeder = seeder_class(db)

        if not await seeder.should_run():
            print(f"⊘ Skipping {name} (already seeded)")
            return False

        print(f"▶ Running {name}...")
        await seeder.run()
        print(f"✓ Completed {name}")
        return True

    async def run_all(self, db: AsyncSession, names: list[str] | None = None) -> None:
        """
        Run multiple seeders in dependency order.

        Args:
            db: Database session
            names: Optional list of seeder names to run. If None, runs all.
        """
        if names is None:
            names = list(self._seeders.keys())

        execution_order = self._resolve_dependencies(names)

        print("\n" + "=" * 60)
        print(f"EXECUTING {len(execution_order)} SEEDERS")
        print("=" * 60 + "\n")

        for name in execution_order:
            await self.run_seeder(name, db)

        print("\n" + "=" * 60)
        print("✓ All seeders completed successfully!")
        print("=" * 60 + "\n")


# Global registry instance
registry = SeederRegistry()
