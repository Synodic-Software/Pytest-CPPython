"""
Shared definitions for testing.
"""


import logging
from pathlib import Path
from typing import Type

from cppython_core.schema import (
    ConfigurePreset,
    CPPythonDataResolved,
    Generator,
    GeneratorConfiguration,
    GeneratorData,
    GeneratorDataResolved,
    GeneratorDataT,
    Interface,
    InterfaceConfiguration,
    PEP621Resolved,
    ProjectConfiguration,
)

test_logger = logging.getLogger(__name__)
test_configuration = GeneratorConfiguration(root_directory=Path())


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


class MockGeneratorDataResolved(GeneratorDataResolved):
    """
    Mock resolved generator data class
    """


class MockGeneratorData(GeneratorData[MockGeneratorDataResolved]):
    """
    Mock generator data class
    """

    def resolve(self, project_configuration: ProjectConfiguration) -> MockGeneratorDataResolved:
        return MockGeneratorDataResolved()


test_generator = MockGeneratorData()


class MockGenerator(Generator[MockGeneratorData, MockGeneratorDataResolved]):
    """
    A mock generator class for behavior testing
    """

    def __init__(
        self,
        configuration: GeneratorConfiguration,
        project: PEP621Resolved,
        cppython: CPPythonDataResolved,
        generator: MockGeneratorDataResolved,
    ) -> None:
        super().__init__(configuration, project, cppython, generator)

        self.downloaded = False

    @staticmethod
    def name() -> str:
        return "mock"

    @staticmethod
    def data_type() -> Type[MockGeneratorData]:
        return MockGeneratorData

    @staticmethod
    def resolved_data_type() -> Type[MockGeneratorDataResolved]:
        return MockGeneratorDataResolved

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

    def generate_cmake_config(self) -> ConfigurePreset:
        return ConfigurePreset(name="mock-config")
