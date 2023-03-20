"""Shared definitions for testing.
"""

from typing import Any

from cppython_core.plugin_schema.generator import (
    Generator,
    GeneratorPluginGroupData,
    SupportedGeneratorFeatures,
)
from cppython_core.schema import CorePluginData, CPPythonModel, Information, SyncData
from pydantic import DirectoryPath


class MockSyncData(SyncData):
    """A Mock data type"""


class MockGeneratorData(CPPythonModel):
    """Dummy data"""


class MockGenerator(Generator):
    """A mock generator class for behavior testing"""

    def __init__(
        self, group_data: GeneratorPluginGroupData, core_data: CorePluginData, configuration_data: dict[str, Any]
    ) -> None:
        self.group_data = group_data
        self.core_data = core_data
        self.configuration_data = MockGeneratorData(**configuration_data)

    @staticmethod
    def features(directory: DirectoryPath) -> SupportedGeneratorFeatures:
        """Broadcasts the shared features of the generator plugin to CPPython

        Args:
            directory: The root directory where features are evaluated

        Returns:
            The supported features
        """
        return SupportedGeneratorFeatures()

    @staticmethod
    def information() -> Information:
        """Returns plugin information

        Returns:
            The plugin information
        """
        return Information()

    @staticmethod
    def sync_types() -> list[type[SyncData]]:
        """_summary_

        Returns:
            _description_
        """

        return [MockSyncData]

    def sync(self, sync_data: SyncData) -> None:
        """Synchronizes generator files and state with the providers input

        Args:
            sync_data: List of information gathered from providers
        """
