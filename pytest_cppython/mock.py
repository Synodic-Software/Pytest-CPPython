"""Shared definitions for testing.
"""

import logging
from pathlib import Path
from typing import Any

from cppython_core.schema import (
    CPPythonDataResolved,
    Generator,
    GeneratorData,
    GeneratorDataResolved,
    Interface,
    PEP621Resolved,
    ProjectConfiguration,
    Provider,
    ProviderConfiguration,
    ProviderData,
    ProviderDataResolved,
    ProviderDataT,
    VersionControl,
    VersionControlData,
    VersionControlDataResolved,
)
from pydantic import Field

test_logger = logging.getLogger(__name__)
test_configuration = ProviderConfiguration(root_directory=Path())


class MockInterface(Interface):
    """A mock interface class for behavior testing"""

    @staticmethod
    def name() -> str:
        """The name of the plugin, canonicalized

        Returns:
            Plugin name
        """
        return "mock"

    def read_provider_data(self, provider_data_type: type[ProviderDataT]) -> ProviderDataT:
        """Implementation of Interface function

        Args:
            provider_data_type: _description_

        Returns:
            _description_
        """

        return provider_data_type()

    def write_pyproject(self) -> None:
        """Implementation of Interface function"""


class MockProviderDataResolved(ProviderDataResolved):
    """Mock resolved provider data class"""

    data_out: bool = Field(description="Value to force resolution type change")


class MockProviderData(ProviderData[MockProviderDataResolved]):
    """Mock provider data class"""

    data_out: Any = Field(default=None, description="Value to force resolution type change + alias", alias="data-out")

    def resolve(self, project_configuration: ProjectConfiguration) -> MockProviderDataResolved:
        """Creates a copy and resolves dynamic attributes

        Args:
            project_configuration: The configuration data used to help the resolution

        Returns:
            The resolved provider data type
        """

        mock_data: bool = self.data_out is None

        return MockProviderDataResolved(data_out=mock_data)


class MockProvider(Provider[MockProviderData, MockProviderDataResolved]):
    """A mock provider class for behavior testing"""

    downloaded: Path | None = None

    def __init__(
        self,
        configuration: ProviderConfiguration,
        project: PEP621Resolved,
        cppython: CPPythonDataResolved,
        provider: MockProviderDataResolved,
    ) -> None:
        super().__init__(configuration, project, cppython, provider)

    @staticmethod
    def name() -> str:
        """The name of the plugin, canonicalized

        Returns:
            The plugin name
        """
        return "mock"

    @staticmethod
    def data_type() -> type[MockProviderData]:
        """Returns the pydantic type to cast the provider configuration data to

        Returns:
            The type
        """
        return MockProviderData

    @staticmethod
    def resolved_data_type() -> type[MockProviderDataResolved]:
        """Returns the pydantic type to cast the resolved provider configuration data to

        Returns:
            The resolved type
        """
        return MockProviderDataResolved

    @classmethod
    def tooling_downloaded(cls, path: Path) -> bool:
        """Returns whether the provider tooling needs to be downloaded

        Args:
            path: The directory to check for downloaded tooling

        Returns:
            Whether the tooling has been downloaded or not
        """
        return cls.downloaded == path

    @classmethod
    async def download_tooling(cls, path: Path) -> None:
        cls.downloaded = path

    def install(self) -> None:
        pass

    def update(self) -> None:
        pass


class MockGeneratorDataResolved(GeneratorDataResolved):
    """Mocked resolved GeneratorData"""


class MockGeneratorData(GeneratorData[MockGeneratorDataResolved]):
    """Mocked GeneratorData"""


class MockGenerator(Generator):
    """A mock generator class for behavior testing"""

    @staticmethod
    def name() -> str:
        """The plugin name

        Returns:
            The name
        """
        return "mock"


class MockVersionControlDataResolved(VersionControlDataResolved):
    """Mocked resolved VersionControlData"""


class MockVersionControlData(VersionControlData[MockVersionControlDataResolved]):
    """Mocked VersionControlData"""


class MockVersionControl(VersionControl):
    """A mock generator class for behavior testing"""

    @staticmethod
    def name() -> str:
        """The plugin name

        Returns:
            The name
        """
        return "mock"

    def extract_version(self, path: Path) -> str:
        """Extracts the system's version metadata

        Args:
            path: The repository path

        Returns:
            A version
        """
        return "1.0.0"

    def is_repository(self, path: Path) -> bool:
        """Queries repository status of a path

        Args:
            path: The input path to query

        Returns:
            Whether the given path is a repository root
        """
        return False
