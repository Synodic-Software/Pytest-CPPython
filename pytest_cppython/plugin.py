"""Helper fixtures and plugin definitions for pytest
"""

import asyncio
from abc import ABC
from importlib.metadata import entry_points
from pathlib import Path
from typing import Generic

import pytest
from cppython_core.plugin_schema.generator import (
    GeneratorConfiguration,
    GeneratorDataT,
    GeneratorT,
)
from cppython_core.plugin_schema.interface import InterfaceT
from cppython_core.plugin_schema.provider import (
    ProviderConfiguration,
    ProviderDataT,
    ProviderT,
)
from cppython_core.plugin_schema.vcs import (
    VersionControlConfiguration,
    VersionControlDataT,
    VersionControlT,
)
from cppython_core.schema import (
    DataPluginT,
    PluginDataConfigurationT,
    PluginDataT,
    PluginT,
    ProjectConfiguration,
    PyProject,
)

from pytest_cppython.fixtures import CPPythonFixtures


class PluginTests(CPPythonFixtures, ABC, Generic[PluginT]):
    """Shared testing information for all plugin test classes"""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[PluginT]:
        """A required testing hook that allows type generation"""

        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="plugin")
    def fixture_plugin(self, plugin_type: type[PluginT]) -> PluginT:
        """A hook allowing implementations to override the fixture

        Args:
            plugin_type: An input interface type

        Returns:
            A newly constructed plugin
        """
        raise NotImplementedError("Subclasses should override this fixture")


class PluginIntegrationTests(PluginTests[PluginT]):
    """Integration testing information for all plugin test classes"""


class PluginUnitTests(PluginTests[PluginT]):
    """Unit testing information for all plugin test classes"""


class DataPluginTests(PluginTests[DataPluginT], Generic[PluginDataConfigurationT, DataPluginT, PluginDataT]):
    """Shared testing information for all data plugin test classes"""

    @pytest.fixture(name="plugin_configuration", scope="session")
    def fixture_plugin_configuration(
        self,
    ) -> PluginDataConfigurationT:
        """A required testing hook that allows plugin configuration data generation"""

        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="plugin_data", scope="session")
    def fixture_plugin_data(
        self,
    ) -> PluginDataT:
        """A required testing hook that allows plugin data generation"""

        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="plugin")
    def fixture_plugin(
        self,
        plugin_type: type[DataPluginT],
        plugin_data: PluginDataT,
        plugin_configuration: PluginDataConfigurationT,
        project: PyProject,
        workspace: ProjectConfiguration,
    ) -> DataPluginT:
        """Overridden plugin generator for creating a populated data plugin type

        Args:
            plugin_type: Plugin type
            plugin_data: Plugin data
            plugin_configuration: Plugin configuration data
            project: Generated static project definition
            workspace: Temporary directory defined by a configuration object

        Returns:
            A newly constructed provider
        """

        assert project.tool is not None
        assert project.tool.cppython is not None

        modified_project_data = project.project.resolve(workspace)
        modified_cppython_data = project.tool.cppython.resolve(workspace)
        modified_cppython_data = modified_cppython_data.resolve_plugin(plugin_type)
        modified_provider_data = plugin_data.resolve(workspace)

        return plugin_type(plugin_configuration, modified_project_data, modified_cppython_data, modified_provider_data)


class DataPluginIntegrationTests(
    PluginIntegrationTests[DataPluginT], DataPluginTests[PluginDataConfigurationT, DataPluginT, PluginDataT]
):
    """Integration testing information for all data plugin test classes"""


class DataPluginUnitTests(
    PluginUnitTests[DataPluginT], DataPluginTests[PluginDataConfigurationT, DataPluginT, PluginDataT]
):
    """Unit testing information for all data plugin test classes"""

    def test_plugin_registration(self, plugin: DataPluginT) -> None:
        """Test the registration with setuptools entry_points

        Args:
            plugin: A newly constructed provider
        """
        plugin_entries = entry_points(group=f"cppython.{plugin.group()}")
        assert len(plugin_entries) > 0

    def test_data_construction(
        self, project: PyProject, plugin_data: PluginDataT, plugin: DataPluginT, plugin_type: type[DataPluginT]
    ) -> None:
        """Tests that the pyproject cant correctly accept and extract the plugin data

        Args:
            project: Test project fixture
            plugin_data: The overridden plugin data
            plugin: The overridden plugin,
            plugin_type: The overridden plugin type
        """
        project_data = project.dict(by_alias=True)

        project_data["tool"]["cppython"]["provider"][plugin.name()] = plugin_data.dict(by_alias=True)
        result = PyProject(**project_data)

        assert result.tool is not None
        assert result.tool.cppython is not None
        assert result.tool.cppython.provider is not None

        data = result.tool.cppython.extract_plugin_data(plugin_type, plugin.data_type())

        assert data.dict(by_alias=True) == plugin_data.dict(by_alias=True)
        assert data.dict() == plugin_data.dict()


class InterfaceTests(PluginTests[InterfaceT]):
    """Shared functionality between the different Interface testing categories"""

    @pytest.fixture(name="plugin")
    def fixture_plugin(self, plugin_type: type[InterfaceT]) -> InterfaceT:
        """Fixture creating the interface.
        Args:
            plugin_type: An input interface type
        Returns:
            A newly constructed interface
        """
        return plugin_type()


class InterfaceIntegrationTests(PluginIntegrationTests[InterfaceT], InterfaceTests[InterfaceT]):
    """Base class for all interface integration tests that test plugin agnostic behavior"""


class InterfaceUnitTests(PluginUnitTests[InterfaceT], InterfaceTests[InterfaceT]):
    """Custom implementations of the Interface class should inherit from this class for its tests.
    Base class for all interface unit tests that test plugin agnostic behavior
    """


class ProviderTests(DataPluginTests[ProviderConfiguration, ProviderT, ProviderDataT]):
    """Shared functionality between the different Provider testing categories"""


class ProviderIntegrationTests(
    DataPluginIntegrationTests[ProviderConfiguration, ProviderT, ProviderDataT],
    ProviderTests[ProviderT, ProviderDataT],
):
    """Base class for all provider integration tests that test plugin agnostic behavior"""

    @pytest.fixture(autouse=True, scope="session")
    def _fixture_install_dependency(self, plugin_type: type[ProviderT], install_path: Path) -> None:
        """Forces the download to only happen once per test session"""

        path = install_path / plugin_type.name()
        path.mkdir(parents=True, exist_ok=True)

        asyncio.run(plugin_type.download_tooling(path))

    def test_is_downloaded(self, plugin: ProviderT) -> None:
        """Verify the plugin is downloaded from fixture

        Args:
            plugin: A newly constructed provider
        """

        assert plugin.tooling_downloaded(plugin.cppython.install_path)

    def test_not_downloaded(self, plugin_type: type[ProviderT], tmp_path: Path) -> None:
        """Verify the provider can identify an empty tool

        Args:
            plugin_type: An input provider type
            tmp_path: A temporary path for the lifetime of the function
        """

        assert not plugin_type.tooling_downloaded(tmp_path)

    def test_install(self, plugin: ProviderT) -> None:
        """Ensure that the vanilla install command functions

        Args:
            plugin: A newly constructed provider
        """
        plugin.install()

    def test_update(self, plugin: ProviderT) -> None:
        """Ensure that the vanilla update command functions

        Args:
            plugin: A newly constructed provider
        """
        plugin.update()


class ProviderUnitTests(
    DataPluginUnitTests[ProviderConfiguration, ProviderT, ProviderDataT],
    ProviderTests[ProviderT, ProviderDataT],
):
    """Custom implementations of the Provider class should inherit from this class for its tests.
    Base class for all provider unit tests that test plugin agnostic behavior
    """


class GeneratorTests(DataPluginTests[GeneratorConfiguration, GeneratorT, GeneratorDataT]):
    """Shared functionality between the different Generator testing categories"""


class GeneratorIntegrationTests(
    DataPluginIntegrationTests[GeneratorT, GeneratorDataT], GeneratorTests[GeneratorT, GeneratorDataT]
):
    """Base class for all vcs integration tests that test plugin agnostic behavior"""


class GeneratorUnitTests(DataPluginUnitTests[GeneratorT, GeneratorDataT], GeneratorTests[GeneratorT, GeneratorDataT]):
    """Custom implementations of the Generator class should inherit from this class for its tests.
    Base class for all Generator unit tests that test plugin agnostic behavior"""


class VersionControlTests(DataPluginTests[VersionControlConfiguration, VersionControlT, VersionControlDataT]):
    """Shared functionality between the different VersionControl testing categories"""


class VersionControlIntegrationTests(
    DataPluginIntegrationTests[VersionControlT, VersionControlDataT],
    VersionControlTests[VersionControlT, VersionControlDataT],
):
    """Base class for all generator integration tests that test plugin agnostic behavior"""


class VersionControlUnitTests(
    DataPluginUnitTests[VersionControlT, VersionControlDataT], VersionControlTests[VersionControlT, VersionControlDataT]
):
    """Custom implementations of the Generator class should inherit from this class for its tests.
    Base class for all Generator unit tests that test plugin agnostic behavior
    """

    def test_not_repository(self, plugin: VersionControlT, tmp_path: Path) -> None:
        """Tests that the temporary directory path will not be registered as a repository

        Args:
            plugin: The VCS constructed type
            tmp_path: Temporary directory
        """

        assert not plugin.is_repository(tmp_path)
