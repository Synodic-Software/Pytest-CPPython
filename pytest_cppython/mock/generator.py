"""Shared definitions for testing.
"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.generator import Generator
from cppython_core.schema import Information, SyncData


class MockSyncData(SyncData):
    """A Mock data type"""


class MockGenerator(Generator):
    """A mock generator class for behavior testing"""

    def activate(self, configuration_data: dict[str, Any]) -> None:
        pass

    @staticmethod
    def supported(directory: Path) -> bool:
        """Mocks support

        Args:
            directory: The input directory

        Returns:
            True, always.
        """
        return True

    @staticmethod
    def information() -> Information:
        """Returns plugin information

        Returns:
            The plugin information
        """
        return Information()

    def sync(self, sync_data: SyncData) -> None:
        """Synchronizes generator files and state with the providers input

        Args:
            sync_data: List of information gathered from providers
        """
