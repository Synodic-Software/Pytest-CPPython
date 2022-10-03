"""Direct Fixtures
"""

from pathlib import Path
from typing import Any, cast

import pytest
from cppython_core.plugin_schema.generator import GeneratorConfiguration
from cppython_core.plugin_schema.provider import ProviderConfiguration
from cppython_core.plugin_schema.vcs import VersionControlConfiguration
from cppython_core.schema import (
    PEP621,
    CPPythonData,
    ProjectConfiguration,
    PyProject,
    ToolData,
)

from pytest_cppython.fixture_data.configuration import (
    generator_config_test_list,
    provider_config_test_list,
    vcs_config_test_list,
)
from pytest_cppython.fixture_data.cppython import cppython_test_list
from pytest_cppython.fixture_data.pep621 import pep621_test_list
from pytest_cppython.mock import MockGenerator, MockProvider, MockVersionControl


class CPPythonFixtures:
    """Fixtures available to CPPython test classes"""

    @pytest.fixture(name="workspace")
    def fixture_workspace(self, tmp_path_factory: pytest.TempPathFactory) -> ProjectConfiguration:
        """Fixture that creates a project configuration at 'workspace/test_project/pyproject.toml'

        Args:
            tmp_path_factory: Factory for centralized temporary directories

        Returns:
            A project configuration that has populated a function level temporary directory
        """
        tmp_path = tmp_path_factory.mktemp("workspace-")

        pyproject_path = tmp_path / "test_project"
        pyproject_path.mkdir(parents=True)
        pyproject_file = pyproject_path / "pyproject.toml"
        pyproject_file.write_text("Test Project File", encoding="utf-8")

        configuration = ProjectConfiguration(pyproject_file=pyproject_file, version="0.1.0")
        return configuration

    @pytest.fixture(
        name="pep621",
        scope="session",
        params=pep621_test_list,
    )
    def fixture_pep621(self, request: pytest.FixtureRequest) -> PEP621:
        """Fixture defining all testable variations of PEP621

        Args:
            request: Parameterization list

        Returns:
            PEP621 variant
        """

        return cast(PEP621, request.param)

    @pytest.fixture(
        name="install_path",
        scope="session",
    )
    def fixture_install_path(self, tmp_path_factory: pytest.TempPathFactory) -> Path:
        """Creates temporary install location

        Args:
            tmp_path_factory: Factory for centralized temporary directories

        Returns:
            A temporary directory
        """
        path = tmp_path_factory.getbasetemp()
        path.mkdir(parents=True, exist_ok=True)

        return path

    @pytest.fixture(
        name="cppython",
        scope="session",
        params=cppython_test_list,
    )
    def fixture_cppython(self, request: pytest.FixtureRequest, install_path: Path) -> CPPythonData:
        """Fixture defining all testable variations of CPPythonData

        Args:
            request: Parameterization list
            install_path: The temporary install directory

        Returns:
            Variation of CPPython data
        """
        cppython_data = cast(CPPythonData, request.param)

        # Pin the install location to the base temporary directory
        cppython_data.install_path = install_path

        return cppython_data

    @pytest.fixture(
        name="provider_configuration",
        scope="session",
        params=provider_config_test_list,
    )
    def fixture_provider_config(self, request: pytest.FixtureRequest) -> ProviderConfiguration:
        """Fixture defining all testable variations of ProviderConfiguration

        Args:
            request: Parameterization list

        Returns:
            Variation of provider configuration data
        """

        return cast(ProviderConfiguration, request.param)

    @pytest.fixture(
        name="generator_configuration",
        scope="session",
        params=generator_config_test_list,
    )
    def fixture_generator_config(self, request: pytest.FixtureRequest) -> GeneratorConfiguration:
        """Fixture defining all testable variations of GeneratorConfiguration

        Args:
            request: Parameterization list

        Returns:
            Variation of generator configuration data
        """

        return cast(GeneratorConfiguration, request.param)

    @pytest.fixture(
        name="version_control_configuration",
        scope="session",
        params=vcs_config_test_list,
    )
    def fixture_vcs_config(self, request: pytest.FixtureRequest) -> VersionControlConfiguration:
        """Fixture defining all testable variations of VersionControlConfiguration

        Args:
            request: Parameterization list

        Returns:
            Variation of vcs configuration data
        """

        return cast(VersionControlConfiguration, request.param)

    @pytest.fixture(name="tool", scope="session")
    def fixture_tool(self, cppython: CPPythonData) -> ToolData:
        """The tool data

        Args:
            cppython: The parameterized cppython table

        Returns:
            Wrapped CPPython data
        """

        return ToolData(cppython=cppython)

    @pytest.fixture(name="project", scope="session")
    def fixture_project(self, tool: ToolData, pep621: PEP621) -> PyProject:
        """Parameterized construction of PyProject data

        Args:
            tool: The tool table with internal cppython data
            pep621: The project table

        Returns:
            All the data as one object
        """

        return PyProject(project=pep621, tool=tool)

    @pytest.fixture(name="project_with_mocks", scope="session")
    def fixture_project_with_mocks(self, project: PyProject) -> dict[str, Any]:
        """Extension of the 'project' fixture with mock data attached

        Args:
            project: The input project

        Returns:
            All the data as a dictionary
        """

        mocked_pyproject = project.dict(by_alias=True)
        mocked_pyproject["tool"]["cppython"]["provider"][MockProvider.name()] = {}
        mocked_pyproject["tool"]["cppython"]["generator"][MockGenerator.name()] = {}
        mocked_pyproject["tool"]["cppython"]["vcs"][MockVersionControl.name()] = {}

        return mocked_pyproject
