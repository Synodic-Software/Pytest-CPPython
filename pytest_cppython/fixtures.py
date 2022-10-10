"""Direct Fixtures
"""

from pathlib import Path
from typing import cast

import pytest
from cppython_core.resolution import (
    resolve_cppython,
    resolve_pep621,
    resolve_project_configuration,
)
from cppython_core.schema import (
    CPPythonData,
    CPPythonGlobalConfiguration,
    CPPythonLocalConfiguration,
    PEP621Configuration,
    PEP621Data,
    ProjectConfiguration,
    ProjectData,
)


class CPPythonFixtures:
    """Fixtures available to CPPython test classes"""

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

    @staticmethod
    def _project_configuration_list() -> list[ProjectConfiguration]:
        """_summary_

        Returns:
            A list of variants to test
        """
        variants = []

        # Use this plugins pyproject file for setup
        variants.append(ProjectConfiguration(pyproject_file=Path("pyproject.toml"), version="0.1.0"))

        return variants

    @pytest.fixture(
        name="project_configuration",
        params=_project_configuration_list(),
        scope="session",
    )
    def fixture_project_configuration(self, request: pytest.FixtureRequest) -> ProjectConfiguration:
        """Fixture that creates a project configuration at 'workspace/test_project/pyproject.toml'

        Args:
            request: Parameterized data

        Returns:
            A project configuration that has populated a function level temporary directory
        """

        return cast(ProjectConfiguration, request.param)

    @staticmethod
    def _pep621_configuration_list() -> list[PEP621Configuration]:
        """_summary_

        Returns:
            A list of variants to test
        """
        variants = []

        variants.append(PEP621Configuration(name="default-test", version="1.0.0"))

        return variants

    @pytest.fixture(
        name="pep621_configuration",
        scope="session",
        params=_pep621_configuration_list(),
    )
    def fixture_pep621_configuration(self, request: pytest.FixtureRequest) -> PEP621Configuration:
        """Fixture defining all testable variations of PEP621

        Args:
            request: Parameterization list

        Returns:
            PEP621 variant
        """

        return cast(PEP621Configuration, request.param)

    @pytest.fixture(
        name="pep621_data",
        scope="session",
    )
    def fixture_pep621_data(
        self, pep621_configuration: PEP621Configuration, project_configuration: ProjectConfiguration
    ) -> PEP621Data:
        """_summary_

        Args:
            pep621_configuration: _description_
            project_configuration: _description_

        Returns:
            _description_
        """

        return resolve_pep621(pep621_configuration, project_configuration)

    @staticmethod
    def _cppython_local_configuration_list() -> list[CPPythonLocalConfiguration]:
        """_summary_

        Returns:
            A list of variants to test
        """
        variants = []

        variants.append(CPPythonLocalConfiguration())

        return variants

    @pytest.fixture(
        name="cppython_local_configuration",
        scope="session",
        params=_cppython_local_configuration_list(),
    )
    def fixture_cppython_local_configuration(
        self, request: pytest.FixtureRequest, install_path: Path
    ) -> CPPythonLocalConfiguration:
        """Fixture defining all testable variations of CPPythonData

        Args:
            request: Parameterization list
            install_path: TODO

        Returns:
            Variation of CPPython data
        """
        cppython_local_configuration = cast(CPPythonLocalConfiguration, request.param)

        data = cppython_local_configuration.dict(by_alias=True)

        # Pin the install location to the base temporary directory
        data["install-path"] = install_path

        return CPPythonLocalConfiguration(**data)

    @staticmethod
    def _cppython_global_configuration_list() -> list[CPPythonGlobalConfiguration]:
        """_summary_

        Returns:
            A list of variants to test
        """
        variants = []

        data = {"current-check": False}

        variants.append(CPPythonGlobalConfiguration(**data))

        return variants

    @pytest.fixture(
        name="cppython_global_configuration",
        scope="session",
        params=_cppython_global_configuration_list(),
    )
    def fixture_cppython_global_configuration(self, request: pytest.FixtureRequest) -> CPPythonGlobalConfiguration:
        """Fixture defining all testable variations of CPPythonData

        Args:
            request: Parameterization list

        Returns:
            Variation of CPPython data
        """
        cppython_global_configuration = cast(CPPythonGlobalConfiguration, request.param)

        return cppython_global_configuration

    @pytest.fixture(
        name="cppython_data",
    )
    def fixture_cppython_data(
        self,
        cppython_local_configuration: CPPythonLocalConfiguration,
        cppython_global_configuration: CPPythonGlobalConfiguration,
        workspace: ProjectData,
    ) -> CPPythonData:
        """_summary_

        Args:
            cppython_local_configuration: _description_
            cppython_global_configuration: _description_
            workspace: _description_

        Returns:
            _description_
        """

        return resolve_cppython(cppython_local_configuration, cppython_global_configuration, workspace)

    @pytest.fixture(name="workspace")
    def fixture_workspace(
        self, project_configuration: ProjectConfiguration, tmp_path_factory: pytest.TempPathFactory
    ) -> ProjectData:
        """Fixture that creates a project space at 'workspace/test_project/pyproject.toml'
        Args:
            project_configuration: Project data
            tmp_path_factory: Factory for centralized temporary directories
        Returns:
            A project data object that has populated a function level temporary directory
        """
        tmp_path = tmp_path_factory.mktemp("workspace-")
        pyproject_path = tmp_path / "test_project"
        pyproject_path.mkdir(parents=True)
        pyproject_file = pyproject_path / "pyproject.toml"
        pyproject_file.write_text("Test Project File", encoding="utf-8")

        configuration = project_configuration.dict()

        # Pin the project location
        configuration["pyproject_file"] = pyproject_file

        data = ProjectConfiguration(**configuration)

        return resolve_project_configuration(data)
