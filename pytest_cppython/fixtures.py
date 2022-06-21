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
    TargetEnum,
)


class CPPythonFixtures:
    """
    Object containing the CPPython data fixtures
    """

    _pep621_parameters: list[tuple[list[str], str | None]] = [([], "1.0.0"), (["version"], None)]

    @pytest.fixture(
        name="pep621",
        scope="session",
        params=_pep621_parameters,
    )
    def fixture_pep621(self, request: pytest.FixtureRequest) -> PEP621:
        """
        Fixture defining all testable variations of Pep621
        """

        dynamic, version = cast(tuple[list[str], str | None], request.param)
        return PEP621(name="test-project", dynamic=dynamic, version=version, description="This is a test description")

    _generator_configuration_parameters: list[Path] = [Path(), Path()]

    @pytest.fixture(
        name="generator_configuration",
        scope="session",
        params=_generator_configuration_parameters,
    )
    def fixture_generator_configuration(self, request: pytest.FixtureRequest) -> GeneratorConfiguration:
        """
        Fixture defining all testable variations of Pep621
        """
        root_path = cast(Path, request.param)
        return GeneratorConfiguration(root_path=root_path)

    _interface_configuration_parameters = []

    @pytest.fixture(
        name="interface_configuration",
        scope="session",
        params=_interface_configuration_parameters,
    )
    def fixture_interface_configuration(self, request: pytest.FixtureRequest) -> InterfaceConfiguration:
        """
        Fixture defining all testable variations of Pep621
        """

        return InterfaceConfiguration()

    _target_parameters = [TargetEnum.EXE, TargetEnum.SHARED, TargetEnum.STATIC]

    @pytest.fixture(
        name="target",
        scope="session",
        params=_target_parameters,
    )
    def fixture_target(self, request: pytest.FixtureRequest) -> TargetEnum:
        """
        Fixture defining all testable variations of CPPythonData
        """
        return cast(TargetEnum, request.param)

    _cppython_parameters = []

    @pytest.fixture(
        name="cppython",
        scope="session",
        params=_cppython_parameters,
    )
    def fixture_cppython(self, request: pytest.FixtureRequest, target: TargetEnum) -> CPPythonData:
        """
        Fixture defining all testable variations of CPPythonData
        """

        return CPPythonData(target=target)
