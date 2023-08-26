"""Composable test types"""

from abc import ABCMeta
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Generic, cast

import pytest
from cppython_core.plugin_schema.generator import (
    Generator,
    GeneratorPluginGroupData,
    GeneratorT,
)
from cppython_core.plugin_schema.provider import (
    Provider,
    ProviderPluginGroupData,
    ProviderT,
)
from cppython_core.plugin_schema.scm import SCM, SCMT, SCMPluginGroupData
from cppython_core.resolution import (
    resolve_cppython_plugin,
    resolve_generator,
    resolve_provider,
    resolve_scm,
)
from cppython_core.schema import (
    CorePluginData,
    CPPythonData,
    CPPythonPluginData,
    DataPluginGroupData,
    DataPluginT,
    PEP621Data,
    PluginGroupData,
    PluginT,
    ProjectConfiguration,
    ProjectData,
)
from synodic_utilities.utility import canonicalize_type

from pytest_cppython.variants import generator_variants, provider_variants, scm_variants


class BaseTests(Generic[PluginT], metaclass=ABCMeta):
    """Shared testing information for all plugin test classes."""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[PluginT]:
        """A required testing hook that allows type generation"""

        raise NotImplementedError("Override this fixture")

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


class BaseIntegrationTests(Generic[PluginT], metaclass=ABCMeta):
    """Integration testing information for all plugin test classes"""

    def test_entry_point(self, plugin_type: type[PluginT]) -> None:
        """Verify that the plugin was registered

        Args:
            plugin_type: The type to register
        """
        group = canonicalize_type(plugin_type).group

        types = []
        for entry in list(entry_points(group=f"cppython.{group}")):
            types.append(entry.load())

        assert plugin_type in types

    def test_name(self, plugin_type: type[PluginT]) -> None:
        """Verifies the the class name allows name extraction

        Args:
            plugin_type: The type to register
        """
        normalized = canonicalize_type(plugin_type)

        assert normalized.group != ""
        assert normalized.name != ""


class BaseUnitTests(Generic[PluginT], metaclass=ABCMeta):
    """Unit testing information for all plugin test classes"""

    def test_feature_extraction(self, plugin_type: type[PluginT], project_configuration: ProjectConfiguration) -> None:
        """_summary_

        Args:
            plugin_type: _description_
            project_configuration: _description_
        """

        assert plugin_type.features(project_configuration.pyproject_file.parent)

    def test_information(self, plugin_type: type[PluginT]) -> None:
        """_summary_

        Args:
            plugin_type: _description_
        """

        assert plugin_type.information()

    def test_plugin_construction(self, plugin: PluginT) -> None:
        """Verifies that the plugin being tested can be constructed

        Args:
            plugin: The data plugin fixture
        """
        assert plugin


class PluginTests(BaseTests[PluginT], Generic[PluginT], metaclass=ABCMeta):
    """Testing information for basic plugin test classes."""

    @staticmethod
    @pytest.fixture(
        name="plugin",
        scope="session",
    )
    def fixture_plugin(
        plugin_type: type[PluginT],
        plugin_group_data: PluginGroupData,
    ) -> PluginT:
        """Overridden plugin generator for creating a populated data plugin type

        Args:
            plugin_type: Plugin type
            plugin_group_data: The data group configuration

        Returns:
            A newly constructed provider
        """

        plugin = plugin_type(plugin_group_data)

        return plugin


class PluginIntegrationTests(BaseIntegrationTests[PluginT], Generic[PluginT], metaclass=ABCMeta):
    """Integration testing information for basic plugin test classes"""


class PluginUnitTests(BaseUnitTests[PluginT], Generic[PluginT], metaclass=ABCMeta):
    """Unit testing information for basic plugin test classes"""


class DataPluginTests(BaseTests[DataPluginT], Generic[DataPluginT], metaclass=ABCMeta):
    """Shared testing information for all data plugin test classes.
    Not inheriting PluginTests to reduce ancestor count
    """

    @staticmethod
    @pytest.fixture(
        name="plugin",
        scope="session",
    )
    def fixture_plugin(
        plugin_type: type[DataPluginT],
        plugin_group_data: DataPluginGroupData,
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


class DataPluginIntegrationTests(BaseIntegrationTests[DataPluginT], Generic[DataPluginT], metaclass=ABCMeta):
    """Integration testing information for all data plugin test classes"""


class DataPluginUnitTests(BaseUnitTests[DataPluginT], Generic[DataPluginT], metaclass=ABCMeta):
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
    def fixture_plugin_configuration_type(self) -> type[ProviderPluginGroupData]:
        """A required testing hook that allows plugin configuration data generation

        Returns:
            The configuration type
        """

        return ProviderPluginGroupData

    @pytest.fixture(name="plugin_group_data", scope="session")
    def fixture_plugin_group_data(self, core_plugin_data: CorePluginData) -> ProviderPluginGroupData:
        """Generates plugin configuration data generation from environment configuration

        Args:
            core_plugin_data: The workspace configuration

        Returns:
            The plugin configuration
        """

        return resolve_provider(core_plugin_data)

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

    @pytest.fixture(
        name="scm_type",
        scope="session",
        params=scm_variants,
    )
    def fixture_scm_type(self, request: pytest.FixtureRequest) -> type[SCM]:
        """Fixture defining all testable variations mock Generator

        Args:
            request: Parameterization list

        Returns:
            Variation of a Generator
        """
        scm_type = cast(type[SCM], request.param)

        return scm_type


class GeneratorTests(DataPluginTests[GeneratorT], Generic[GeneratorT], metaclass=ABCMeta):
    """Shared functionality between the different Generator testing categories"""

    @pytest.fixture(name="plugin_configuration_type", scope="session")
    def fixture_plugin_configuration_type(self) -> type[GeneratorPluginGroupData]:
        """A required testing hook that allows plugin configuration data generation

        Returns:
            The configuration type
        """

        return GeneratorPluginGroupData

    @pytest.fixture(name="plugin_group_data", scope="session")
    def fixture_plugin_group_data(self, core_plugin_data: CorePluginData) -> GeneratorPluginGroupData:
        """Generates plugin configuration data generation from environment configuration

        Args:
            core_plugin_data: The workspace configuration

        Returns:
            The plugin configuration
        """

        return resolve_generator(core_plugin_data)

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

    @pytest.fixture(
        name="scm_type",
        scope="session",
        params=scm_variants,
    )
    def fixture_scm_type(self, request: pytest.FixtureRequest) -> type[SCM]:
        """Fixture defining all testable variations mock Generator

        Args:
            request: Parameterization list

        Returns:
            Variation of a Generator
        """
        scm_type = cast(type[SCM], request.param)

        return scm_type


class SCMTests(PluginTests[SCMT], Generic[SCMT], metaclass=ABCMeta):
    """Shared functionality between the different SCM testing categories"""

    @pytest.fixture(name="plugin_configuration_type", scope="session")
    def fixture_plugin_configuration_type(self) -> type[SCMPluginGroupData]:
        """A required testing hook that allows plugin configuration data generation

        Returns:
            The configuration type
        """

        return SCMPluginGroupData

    @pytest.fixture(name="plugin_group_data", scope="session")
    def fixture_plugin_group_data(self, core_plugin_data: CorePluginData) -> SCMPluginGroupData:
        """Generates plugin configuration data generation from environment configuration

        Args:
            core_plugin_data: The workspace configuration

        Returns:
            The plugin configuration
        """

        return resolve_scm(core_plugin_data)

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

    @pytest.fixture(
        name="scm_type",
        scope="session",
        params=scm_variants,
    )
    def fixture_scm_type(self, plugin_type: type[SCMT]) -> type[SCM]:
        """Fixture defining all testable variations mock Generator

        Args:
            plugin_type: Parameterization list

        Returns:
            Variation of a Generator
        """

        return plugin_type
