"""
Direct Fixtures
"""
from typing import cast

import pytest
from cppython_core.schema import (
    PEP621,
    CPPythonData,
    GeneratorConfiguration,
    InterfaceConfiguration,
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
        TODO
        """
        tmp_path = tmp_path_factory.mktemp("workspace-")
        return tmp_path

    @pytest.fixture(
        name="pep621",
        scope="session",
        params=pep621_test_list,
    )
    def fixture_pep621(self, request: pytest.FixtureRequest) -> PEP621:
        """
        Fixture defining all testable variations of PEP621
        """

        return cast(PEP621, request.param)

    @pytest.fixture(
        name="cppython",
        scope="session",
        params=cppython_test_list,
    )
    def fixture_cppython(self, request: pytest.FixtureRequest) -> CPPythonData:
        """
        Fixture defining all testable variations of CPPythonData
        """

        return cast(CPPythonData, request.param)

    @pytest.fixture(
        name="generator_configuration",
        scope="session",
        params=generator_config_test_list,
    )
    def fixture_generator_config(self, request: pytest.FixtureRequest) -> GeneratorConfiguration:
        """
        Fixture defining all testable variations of GeneratorConfiguration
        """

        return cast(GeneratorConfiguration, request.param)

    @pytest.fixture(
        name="interface_configuration",
        scope="session",
        params=interface_config_test_list,
    )
    def fixture_interface_config(self, request: pytest.FixtureRequest) -> InterfaceConfiguration:
        """
        Fixture defining all testable variations of InterfaceConfiguration
        """

        return cast(InterfaceConfiguration, request.param)
