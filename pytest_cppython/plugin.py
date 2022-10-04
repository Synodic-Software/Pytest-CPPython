"""Helper fixtures and plugin definitions for pytest
"""

import asyncio
from abc import ABC, abstractmethod
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Generic

import pytest
from cppython_core.plugin_schema.generator import GeneratorConfiguration, GeneratorT
from cppython_core.plugin_schema.interface import InterfaceT
from cppython_core.plugin_schema.provider import ProviderConfiguration, ProviderT
from cppython_core.plugin_schema.vcs import VersionControlConfiguration, VersionControlT
from cppython_core.schema import (
    DataPluginT,
    PluginDataConfigurationT,
    PluginT,
    ProjectConfiguration,
    PyProject,
)

from pytest_cppython.fixtures import CPPythonFixtures


class PluginTests(CPPythonFixtures, ABC, Generic[PluginT]):
    """Shared testing information for all plugin test classes"""

    @abstractmethod
    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[PluginT]:
        """A required testing hook that allows type generation"""

        raise NotImplementedError("Subclasses should override this fixture")


class PluginIntegrationTests(PluginTests[PluginT]):
    """Integration testing information for all plugin test classes"""


class PluginUnitTests(PluginTests[PluginT]):
    """Unit testing information for all plugin test classes"""


class DataPluginTests(PluginTests[DataPluginT], Generic[PluginDataConfigurationT, DataPluginT]):
    """Shared testing information for all data plugin test classes"""

    @pytest.fixture(name="mock_project")
    def fixture_mock_project(
        self,
        plugin_type: type[DataPluginT],
        plugin_data: dict[str, Any],
        project: PyProject,
    ) -> PyProject:
        """_summary_

        Args:
            plugin_type: _description_
            plugin_data: _description_
            project: _description_

        Returns:
            _description_
        """

        mock_project = project.copy(deep=True)

        assert mock_project.tool is not None
        assert mock_project.tool.cppython is not None

        plugin_attribute = getattr(mock_project.tool.cppython, plugin_type.group())
        plugin_attribute[plugin_type.name()] = plugin_data

        return mock_project

    @pytest.fixture(name="plugin")
    def fixture_plugin(
        self,
        plugin_type: type[DataPluginT],
        plugin_configuration: PluginDataConfigurationT,
        mock_project: PyProject,
        workspace: ProjectConfiguration,
    ) -> DataPluginT:
        """Overridden plugin generator for creating a populated data plugin type

        Args:
            plugin_type: Plugin type
            plugin_configuration: Plugin configuration data
            mock_project: Generated static project definition
            workspace: Temporary directory defined by a configuration object

        Returns:
            A newly constructed provider
        """

        assert mock_project.tool is not None
        assert mock_project.tool.cppython is not None

        modified_project_data = mock_project.project.resolve(workspace)
        modified_cppython_data = mock_project.tool.cppython.resolve(workspace)
        modified_cppython_data = modified_cppython_data.resolve_plugin(plugin_type)

        plugin_attribute = getattr(mock_project.tool.cppython, plugin_type.group())
        plugin_data = plugin_attribute[plugin_type.name()]

        return plugin_type(plugin_configuration, modified_project_data, modified_cppython_data, plugin_data)


class DataPluginIntegrationTests(
    PluginIntegrationTests[DataPluginT],
    DataPluginTests[PluginDataConfigurationT, DataPluginT],
    Generic[PluginDataConfigurationT, DataPluginT],
):
    """Integration testing information for all data plugin test classes"""


class DataPluginUnitTests(
    PluginUnitTests[DataPluginT],
    DataPluginTests[PluginDataConfigurationT, DataPluginT],
    Generic[PluginDataConfigurationT, DataPluginT],
):
    """Unit testing information for all data plugin test classes"""

    def test_plugin_registration(self, plugin: DataPluginT) -> None:
        """Test the registration with setuptools entry_points

        Args:
            plugin: A newly constructed provider
        """
        plugin_entries = entry_points(group=f"cppython.{plugin.group()}")
        assert len(plugin_entries) > 0


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


class InterfaceIntegrationTests(PluginIntegrationTests[InterfaceT], InterfaceTests[InterfaceT], Generic[InterfaceT]):
    """Base class for all interface integration tests that test plugin agnostic behavior"""


class InterfaceUnitTests(PluginUnitTests[InterfaceT], InterfaceTests[InterfaceT], Generic[InterfaceT]):
    """Custom implementations of the Interface class should inherit from this class for its tests.
    Base class for all interface unit tests that test plugin agnostic behavior
    """


class ProviderTests(DataPluginTests[ProviderConfiguration, ProviderT], Generic[ProviderT]):
    """Shared functionality between the different Provider testing categories"""

    @pytest.fixture(name="plugin_configuration", scope="session")
    def fixture_plugin_configuration(self, provider_configuration: ProviderConfiguration) -> ProviderConfiguration:
        """A required testing hook that allows plugin configuration data generation

        Args:
            provider_configuration: The configuration object

        Returns:
            The configuration object
        """

        return provider_configuration


class ProviderIntegrationTests(
    DataPluginIntegrationTests[ProviderConfiguration, ProviderT],
    ProviderTests[ProviderT],
    Generic[ProviderT],
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
    DataPluginUnitTests[ProviderConfiguration, ProviderT],
    ProviderTests[ProviderT],
    Generic[ProviderT],
):
    """Custom implementations of the Provider class should inherit from this class for its tests.
    Base class for all provider unit tests that test plugin agnostic behavior
    """


class GeneratorTests(DataPluginTests[GeneratorConfiguration, GeneratorT], Generic[GeneratorT]):
    """Shared functionality between the different Generator testing categories"""

    @pytest.fixture(name="plugin_configuration", scope="session")
    def fixture_plugin_configuration(self, generator_configuration: GeneratorConfiguration) -> GeneratorConfiguration:
        """A required testing hook that allows plugin configuration data generation

        Args:
            generator_configuration: The configuration object

        Returns:
            The configuration object
        """

        return generator_configuration


class GeneratorIntegrationTests(
    DataPluginIntegrationTests[GeneratorConfiguration, GeneratorT],
    GeneratorTests[GeneratorT],
    Generic[GeneratorT],
):
    """Base class for all vcs integration tests that test plugin agnostic behavior"""


class GeneratorUnitTests(
    DataPluginUnitTests[GeneratorConfiguration, GeneratorT],
    GeneratorTests[GeneratorT],
    Generic[GeneratorT],
):
    """Custom implementations of the Generator class should inherit from this class for its tests.
    Base class for all Generator unit tests that test plugin agnostic behavior"""


class VersionControlTests(
    DataPluginTests[VersionControlConfiguration, VersionControlT],
    Generic[VersionControlT],
):
    """Shared functionality between the different VersionControl testing categories"""

    @pytest.fixture(name="plugin_configuration", scope="session")
    def fixture_plugin_configuration(
        self, version_control_configuration: VersionControlConfiguration
    ) -> VersionControlConfiguration:
        """A required testing hook that allows plugin configuration data generation

        Args:
            version_control_configuration: The configuration object

        Returns:
            The configuration object
        """

        return version_control_configuration


class VersionControlIntegrationTests(
    DataPluginIntegrationTests[VersionControlConfiguration, VersionControlT],
    VersionControlTests[VersionControlT],
    Generic[VersionControlT],
):
    """Base class for all generator integration tests that test plugin agnostic behavior"""


class VersionControlUnitTests(
    DataPluginUnitTests[VersionControlConfiguration, VersionControlT],
    VersionControlTests[VersionControlT],
    Generic[VersionControlT],
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
