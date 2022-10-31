"""Mock provider definitions"""


from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.provider import Provider
from cppython_core.schema import SyncData


class MockProvider(Provider):
    """A mock provider class for behavior testing"""

    downloaded: Path | None = None

    def activate(self, data: dict[str, Any]) -> None:
        pass

    @staticmethod
    def name() -> str:
        """The name of the plugin, canonicalized

        Returns:
            The plugin name
        """
        return "mock"

    def sync_data(self, generator_name: str) -> SyncData:
        """Gathers synchronization data

        Args:
            generator_name: The input generator name. An implicit token

        Raises:
            NotSupportedError: If not supported

        Returns:
            The sync data object
        """
        return SyncData(data=None, name=self.name())

    @classmethod
    async def download_tooling(cls, path: Path) -> None:
        cls.downloaded = path

    def install(self) -> None:
        pass

    def update(self) -> None:
        pass
