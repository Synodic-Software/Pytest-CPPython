"""
Shared definitions for testing.
TODO: Replace with conftest.py
"""


import logging
from pathlib import Path
from typing import Type

from cppython_core.schema import (
    PEP621,
    ConfigurePreset,
    CPPythonData,
    Generator,
    GeneratorConfiguration,
    GeneratorData,
    GeneratorDataT,
    Interface,
    InterfaceConfiguration,
    ProjectConfiguration,
)

test_logger = logging.getLogger(__name__)
test_configuration = GeneratorConfiguration(root_path=Path())


class MockInterface(Interface):
    """
    A mock interface class for behavior testing
    """

    def __init__(self, configuration: InterfaceConfiguration) -> None:
        super().__init__(configuration)

    @staticmethod
    def name() -> str:
        return "mock"

    def read_generator_data(self, generator_data_type: Type[GeneratorDataT]) -> GeneratorDataT:
        """
        Implementation of Interface function
        """
        return generator_data_type()

    def write_pyproject(self) -> None:
        """
        Implementation of Interface function
        """


class MockGeneratorData(GeneratorData):
    """
    Mock generator data class
    """

    def resolve(self: GeneratorDataT, project_configuration: ProjectConfiguration) -> GeneratorDataT:
        return self


test_generator = MockGeneratorData()


class MockGenerator(Generator[MockGeneratorData]):
    """
    A mock generator class for behavior testing
    """

    def __init__(
        self,
        configuration: GeneratorConfiguration,
        project: PEP621,
        cppython: CPPythonData,
        generator: MockGeneratorData,
    ) -> None:
        super().__init__(configuration, project, cppython, generator)

        self.downloaded = False

    @staticmethod
    def name() -> str:
        return "mock"

    @staticmethod
    def data_type() -> Type[MockGeneratorData]:
        return MockGeneratorData

    def generator_downloaded(self, path: Path) -> bool:
        return self.downloaded

    def download_generator(self, path: Path) -> None:
        self.downloaded = True

    def update_generator(self, path: Path) -> None:
        pass

    def install(self) -> None:
        pass

    def update(self) -> None:
        pass

    def build(self) -> None:
        pass

    def generate_cmake_config(self) -> ConfigurePreset:
        return ConfigurePreset(name="mock-config")
