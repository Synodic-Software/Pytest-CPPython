"""Composable test types"""

from abc import ABCMeta
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Generic, cast

import pytest
from cppython_core.plugin_schema.generator import (
    Generator,
    GeneratorGroupData,
    GeneratorT,
)
from cppython_core.plugin_schema.provider import Provider, ProviderGroupData, ProviderT
from cppython_core.plugin_schema.scm import SCMT
from cppython_core.resolution import (
    resolve_cppython_plugin,
    resolve_full_name,
    resolve_generator,
    resolve_group,
    resolve_provider,
)
from cppython_core.schema import (
    CorePluginData,
    CPPythonData,
    CPPythonPluginData,
    DataPluginT,
    Information,
    PEP621Data,
    PluginGroupData,
    PluginT,
    ProjectData,
)

from pytest_cppython.variants import generator_variants, provider_variants


class PluginTests(Generic[PluginT], metaclass=ABCMeta):
    """Shared testing information for all plugin test classes."""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[PluginT]:
        """A required testing hook that allows type generation"""

        raise NotImplementedError("Override this fixture")

    @pytest.fixture(name="plugin_information", scope="session")
    def fixture_plugin_information(self, plugin_type: type[PluginT]) -> Information:
        """Helper to extract the plugin information

        Args:
            plugin_type: The type to extract

        Returns:
            The plugin's information
        """

        return plugin_type.information()


class PluginIntegrationTests(Generic[PluginT], metaclass=ABCMeta):
    """Integration testing information for all plugin test classes"""

    def test_entry_point(self, plugin_type: type[PluginT]) -> None:
        """Verify that the plugin was registered

        Args:
            plugin_type: The type to register
        """
        group = resolve_group(plugin_type)

        types = []
        for entry in list(entry_points(group=f"cppython.{group}")):
            types.append(entry.load())

        assert plugin_type in types

    def test_name_length(self, plugin_type: type[PluginT]) -> None:
        """Verifies that the name follows group conventions

        Args:
            plugin_type: The type to parse
        """

        name = resolve_full_name(plugin_type)

        split_name = str(name).split(".")

        assert len(split_name) == 2, (
            "The plugin class name must only consist of two elements in PascalCase - the plugin name and the plugin"
            " group"
        )


class PluginUnitTests(Generic[PluginT], metaclass=ABCMeta):
    """Unit testing information for all plugin test classes"""

    def test_not_supported(self, plugin_type: type[PluginT], tmp_path: Path) -> None:
        """Tests that the temporary directory path will not be registered as supported

        Args:
            plugin_type: The plugin type
            tmp_path: Temporary directory
        """

        assert not plugin_type.supported(tmp_path)

    def test_wont_initialize(self, plugin_information: Information) -> None:
        """Prevent initialization from being set

        Args:
            plugin_information: The plugin information
        """

        assert not plugin_information.initialization, "Keep 'initialization' False. The feature is under development"


class DataPluginTests(PluginTests[DataPluginT], Generic[DataPluginT], metaclass=ABCMeta):
    """Shared testing information for all data plugin test classes.
    Not inheriting PluginTests to reduce ancestor count
    """

    @pytest.fixture(
        name="cppython_plugin_data",
        scope="session",
    )
    def fixture_cppython_plugin_data(
        self, cppython_data: CPPythonData, plugin_type: type[DataPluginT]
    ) -> CPPythonPluginData:
        """Fixture for created the plugin CPPython table

        Args:
            cppython_data: The CPPython table to help the resolve
            plugin_type: The data plugin type

        Returns:
            The plugin specific CPPython table information
        """

        return resolve_cppython_plugin(cppython_data, plugin_type)

    @pytest.fixture(
        name="core_plugin_data",
        scope="session",
    )
    def fixture_core_plugin_data(
        self, cppython_plugin_data: CPPythonPluginData, project_data: ProjectData, pep621_data: PEP621Data
    ) -> CorePluginData:
        """Fixture for creating the wrapper CoreData type

        Args:
            cppython_plugin_data: CPPython data
            project_data: The project data
            pep621_data: Project table data

        Returns:
            Wrapper Core Type
        """

        return CorePluginData(cppython_data=cppython_plugin_data, project_data=project_data, pep621_data=pep621_data)

    @staticmethod
    @pytest.fixture(
        name="plugin",
        scope="session",
    )
    def fixture_plugin(
        plugin_type: type[DataPluginT],
        plugin_group_data: PluginGroupData,
        core_plugin_data: CorePluginData,
        plugin_data: dict[str, Any],
    ) -> DataPluginT:
        """Overridden plugin generator for creating a populated data plugin type

        Args:
            plugin_type: Plugin type
            plugin_group_data: The data group configuration
            core_plugin_data: The core metadata
            plugin_data: The data table

        Returns:
            A newly constructed provider
        """

        plugin = plugin_type(plugin_group_data, core_plugin_data, plugin_data)

        return plugin


class DataPluginIntegrationTests(PluginIntegrationTests[DataPluginT], Generic[DataPluginT], metaclass=ABCMeta):
    """Integration testing information for all data plugin test classes"""


class DataPluginUnitTests(PluginUnitTests[DataPluginT], Generic[DataPluginT], metaclass=ABCMeta):
    """Unit testing information for all data plugin test classes"""

    def test_pyproject_undefined(self, plugin_data_path: Path | None) -> None:
        """Verifies that the directory data provided by plugins does not contain a pyproject.toml file

        Args:
            plugin_data_path: The plugin's tests/data directory
        """

        if plugin_data_path is not None:
            paths = list(plugin_data_path.rglob("pyproject.toml"))

            assert not paths


class ProviderTests(DataPluginTests[ProviderT], Generic[ProviderT], metaclass=ABCMeta):
    """Shared functionality between the different Provider testing categories"""

    @pytest.fixture(name="plugin_configuration_type", scope="session")
    def fixture_plugin_configuration_type(self) -> type[ProviderGroupData]:
        """A required testing hook that allows plugin configuration data generation

        Returns:
            The configuration type
        """

        return ProviderGroupData

    @pytest.fixture(name="plugin_group_data", scope="session")
    def fixture_plugin_group_data(self, project_data: ProjectData) -> ProviderGroupData:
        """Generates plugin configuration data generation from environment configuration

        Args:
            project_data: The workspace configuration

        Returns:
            The plugin configuration
        """

        return resolve_provider(project_data)

    @pytest.fixture(
        name="provider_type",
        scope="session",
        params=provider_variants,
    )
    def fixture_provider_type(self, plugin_type: type[ProviderT]) -> type[ProviderT]:
        """Fixture defining all testable variations mock Providers

        Args:
            plugin_type: Plugin type

        Returns:
            Variation of a Provider
        """
        return plugin_type

    @pytest.fixture(
        name="generator_type",
        scope="session",
        params=generator_variants,
    )
    def fixture_generator_type(self, request: pytest.FixtureRequest) -> type[Generator]:
        """Fixture defining all testable variations mock Generator

        Args:
            request: Parameterization list

        Returns:
            Variation of a Generator
        """
        generator_type = cast(type[Generator], request.param)

        return generator_type


class GeneratorTests(DataPluginTests[GeneratorT], Generic[GeneratorT], metaclass=ABCMeta):
    """Shared functionality between the different Generator testing categories"""

    @pytest.fixture(name="plugin_configuration_type", scope="session")
    def fixture_plugin_configuration_type(self) -> type[GeneratorGroupData]:
        """A required testing hook that allows plugin configuration data generation

        Returns:
            The configuration type
        """

        return GeneratorGroupData

    @pytest.fixture(name="plugin_group_data", scope="session")
    def fixture_plugin_group_data(self, project_data: ProjectData) -> GeneratorGroupData:
        """Generates plugin configuration data generation from environment configuration

        Args:
            project_data: The workspace configuration

        Returns:
            The plugin configuration
        """

        return resolve_generator(project_data)

    @pytest.fixture(
        name="provider_type",
        scope="session",
        params=provider_variants,
    )
    def fixture_provider_type(self, request: pytest.FixtureRequest) -> type[Provider]:
        """Fixture defining all testable variations mock Providers

        Args:
            request: Parameterization list

        Returns:
            Variation of a Provider
        """
        provider_type = cast(type[Provider], request.param)

        return provider_type

    @pytest.fixture(
        name="generator_type",
        scope="session",
    )
    def fixture_generator_type(self, plugin_type: type[GeneratorT]) -> type[GeneratorT]:
        """Override

        Args:
            plugin_type: Plugin type

        Returns:
            Plugin type
        """

        return plugin_type


class SCMTests(PluginTests[SCMT], Generic[SCMT], metaclass=ABCMeta):
    """Shared functionality between the different SCM testing categories"""

    @pytest.fixture(name="plugin")
    def fixture_plugin(
        self,
        plugin_type: type[SCMT],
    ) -> SCMT:
        """Fixture creating the plugin.
        Args:
            plugin_type: An input plugin type

        Returns:
            A newly constructed plugin
        """
        return plugin_type()
