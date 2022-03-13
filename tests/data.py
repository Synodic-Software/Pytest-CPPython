"""
TODO
"""


from pathlib import Path
from typing import Type

from cppython_core.schema import (
    PEP621,
    CPPythonData,
    Generator,
    GeneratorData,
    GeneratorDataType,
    Interface,
    PyProject,
    ToolData,
)

test_cppython = CPPythonData(**{"generator":"test_generator", "target":"executable", "install-path": Path()})
test_tool = ToolData(cppython=test_cppython)
test_pep621 = PEP621(name="test-project", version="1.0.0", description="This is a test project")
test_pyproject = PyProject(project=test_pep621, tool=test_tool)


class TestInterface(Interface):
    """
    TODO
    """

    def print(self, string: str) -> None:
        """
        TODO
        """

    def read_generator_data(self, generator_data_type: Type[GeneratorDataType]) -> GeneratorDataType:
        """
        TODO
        """
        return generator_data_type()

    def write_pyproject(self) -> None:
        """
        TODO
        """


class TestGenerator(Generator):
    """
    TODO
    """

    def __init__(self, pyproject: PyProject, generator_data: GeneratorData) -> None:
        super().__init__(pyproject, generator_data)

    @staticmethod
    def name() -> str:
        return "test"

    @staticmethod
    def data_type() -> Type[GeneratorData]:
        return GeneratorData

    def generator_downloaded(self) -> bool:
        return True

    def download_generator(self) -> None:
        pass

    def update_generator(self) -> None:
        pass

    def install(self) -> None:
        pass

    def update(self) -> None:
        pass

    def build(self) -> None:
        pass
