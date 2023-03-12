"""Mock provider definitions"""


from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.generator import SyncConsumer
from cppython_core.plugin_schema.provider import Provider, ProviderGroupData
from cppython_core.resolution import resolve_name
from cppython_core.schema import CorePluginData, CPPythonModel, Information, SyncData

from pytest_cppython.mock.generator import MockSyncData


class MockProviderData(CPPythonModel):
    """Dummy data"""


class MockProvider(Provider):
    """A mock provider class for behavior testing"""

    downloaded: Path | None = None

    def __init__(
        self, group_data: ProviderGroupData, core_data: CorePluginData, configuration_data: dict[str, Any]
    ) -> None:
        self.group_data = group_data
        self.core_data = core_data
        self.configuration_data = MockProviderData(**configuration_data)

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

    @staticmethod
    def supported_sync_type(sync_type: type[SyncData]) -> bool:
        """Broadcasts supported types

        Args:
            sync_type: The input type

        Returns:
            Support
        """

        return sync_type == MockSyncData

    def sync_data(self, consumer: SyncConsumer) -> SyncData | None:
        """Gathers synchronization data

        Args:
            consumer: The input consumer

        Returns:
            The sync data object
        """

        # This is a mock class, so any generator sync type is OK
        for sync_type in consumer.sync_types():
            match sync_type:
                case MockSyncData(sync_type):
                    return MockSyncData(provider_name=resolve_name(type(self)))

        return None

    @classmethod
    async def download_tooling(cls, path: Path) -> None:
        cls.downloaded = path

    def install(self) -> None:
        pass

    def update(self) -> None:
        pass
