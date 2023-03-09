"""Shared definitions for testing.
"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.generator import Generator, GeneratorGroupData
from cppython_core.schema import CorePluginData, CPPythonModel, Information, SyncData


class MockSyncData(SyncData):
    """A Mock data type"""


class MockGeneratorData(CPPythonModel):
    """Dummy data"""


class MockGenerator(Generator[MockGeneratorData]):
    """A mock generator class for behavior testing"""

    def __init__(
        self, group_data: GeneratorGroupData, core_data: CorePluginData, configuration_data: dict[str, Any]
    ) -> None:
        self.group_data = group_data
        self.core_data = core_data
        self.configuration_data = MockGeneratorData(**configuration_data)

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
