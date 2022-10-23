"""Shared definitions for testing.
"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.generator import Generator
from cppython_core.schema import SyncData


class MockGenerator(Generator):
    """A mock generator class for behavior testing"""

    @staticmethod
    def name() -> str:
        """The plugin name

        Returns:
            The name
        """
        return "mock"

    def activate(self, data: dict[str, Any]) -> None:
        pass

    @staticmethod
    def is_supported(path: Path) -> bool:
        """Queries generator support of the given path

        Args:
            path: Input path

        Returns:
            True if supported
        """
        return True

    def sync(self, results: list[SyncData]) -> None:
        pass
