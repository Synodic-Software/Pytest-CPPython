"""
Direct Fixtures
"""
from pathlib import Path
from typing import cast

import pytest
from cppython_core.schema import (
    PEP621,
    CPPythonData,
    GeneratorConfiguration,
    InterfaceConfiguration,
    ProjectConfiguration,
)

from pytest_cppython.fixture_data.configuration import (
    generator_config_test_list,
    interface_config_test_list,
)
from pytest_cppython.fixture_data.cppython import cppython_test_list
from pytest_cppython.fixture_data.pep621 import pep621_test_list


class CPPythonFixtures:
    """
    Object containing the CPPython data fixtures
    """

    @pytest.fixture(name="workspace")
    def fixture_workspace(self, tmp_path_factory: pytest.TempPathFactory):
        """
        Fixture that creates a project configuration at 'workspace/test_project/pyproject.toml'
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
        """
        Fixture defining all testable variations of PEP621
        """

        return cast(PEP621, request.param)  # type: ignore

    @pytest.fixture(
        name="install_path",
        scope="session",
    )
    def fixture_install_path(self, tmp_path_factory: pytest.TempPathFactory) -> Path:
        """
        Test install location
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
        """
        Fixture defining all testable variations of CPPythonData
        """
        cppython_data = cast(CPPythonData, request.param)  # type: ignore

        # Pin the install location to the base temporary directory
        cppython_data.install_path = install_path

        return cppython_data

    @pytest.fixture(
        name="generator_configuration",
        scope="session",
        params=generator_config_test_list,
    )
    def fixture_generator_config(self, request: pytest.FixtureRequest) -> GeneratorConfiguration:
        """
        Fixture defining all testable variations of GeneratorConfiguration
        """

        return cast(GeneratorConfiguration, request.param)  # type: ignore

    @pytest.fixture(
        name="interface_configuration",
        scope="session",
        params=interface_config_test_list,
    )
    def fixture_interface_config(self, request: pytest.FixtureRequest) -> InterfaceConfiguration:
        """
        Fixture defining all testable variations of InterfaceConfiguration
        """

        return cast(InterfaceConfiguration, request.param)  # type: ignore
