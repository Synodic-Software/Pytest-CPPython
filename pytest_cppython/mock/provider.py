"""Mock provider definitions"""


from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.provider import Provider
from cppython_core.schema import PluginName, SyncData

from pytest_cppython.mock.base import MockBase
from pytest_cppython.mock.generator import MockSyncData


class MockProvider(Provider, MockBase):
    """A mock provider class for behavior testing"""

    downloaded: Path | None = None

    @staticmethod
    def supported(directory: Path) -> bool:
        """Mocks support

        Args:
            directory: The input directory

        Returns:
            True, always.
        """
        return True

    def activate(self, data: dict[str, Any]) -> None:
        pass

    def sync_data(self, generator_name: PluginName) -> SyncData | None:
        """Gathers synchronization data

        Args:
            generator_name: The input generator name

        Raises:
            NotSupportedError: If not supported

        Returns:
            The sync data object
        """

        # This is a mock class, so any generator sync type is OK
        match generator_name:
            case True:
                return MockSyncData(provider_name=self.name())
            case _:
                return None

    @classmethod
    async def download_tooling(cls, path: Path) -> None:
        cls.downloaded = path

    def install(self) -> None:
        pass

    def update(self) -> None:
        pass
