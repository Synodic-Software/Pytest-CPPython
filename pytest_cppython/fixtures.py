"""
Direct Fixtures
"""
from pathlib import Path
from typing import cast

import pytest
from cppython_core.schema import (
    PEP508,
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

    _generator_configuration_parameters: list[Path] = [Path("/"), Path("/..")]

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

    @pytest.fixture(
        name="interface_configuration",
        scope="session",
    )
    def fixture_interface_configuration(self) -> InterfaceConfiguration:
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
        TODO
        """
        return cast(TargetEnum, request.param)

    _dependency_parameters = [[], [PEP508("poco")]]

    @pytest.fixture(
        name="dependencies",
        scope="session",
        params=_dependency_parameters,
    )
    def fixture_dependencies(self, request: pytest.FixtureRequest) -> list[PEP508]:
        """
        TODO
        """
        return cast(list[PEP508], request.param)

    _install_path_parameters = []

    @pytest.fixture(
        name="install_path",
        scope="session",
        params=_install_path_parameters,
    )
    def fixture_install_path(self, request: pytest.FixtureRequest) -> Path:
        """
        TODO
        """
        return cast(Path, request.param)

    _tool_path_parameters = []

    @pytest.fixture(
        name="tool_path",
        scope="session",
        params=_tool_path_parameters,
    )
    def fixture_tool_path(self, request: pytest.FixtureRequest) -> Path:
        """
        TODO
        """
        return cast(Path, request.param)

    _build_path_parameters = []

    @pytest.fixture(
        name="build_path",
        scope="session",
        params=_build_path_parameters,
    )
    def fixture_build_path(self, request: pytest.FixtureRequest) -> Path:
        """
        TODO
        """
        return cast(Path, request.param)

    @pytest.fixture(name="cppython", scope="session")
    def fixture_cppython(
        self, target: TargetEnum, dependencies: list[PEP508], install_path: Path, tool_path: Path, build_path: Path
    ) -> CPPythonData:
        """
        Fixture defining all testable variations of CPPythonData
        """

        return CPPythonData(
            target=target,
            dependencies=dependencies,
            install_path=install_path,
            tool_path=tool_path,
            build_path=build_path,
        )
