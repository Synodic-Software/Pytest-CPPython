"""Shared definitions for testing.
"""

from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.generator import Generator
from cppython_core.schema import CPPythonModel, SyncData
from pydantic import Field, FilePath


class MockGeneratorData(CPPythonModel):
    """Tests a variety of data conditions"""

    test_file_requirement: FilePath


class MockGeneratorConfiguration(CPPythonModel):
    """Fulfills the defaulting of the FilePath"""

    test_file_requirement: FilePath = Field(default=Path("requirement.txt"))


class MockGenerator(Generator):
    """A mock generator class for behavior testing"""

    @staticmethod
    def name() -> str:
        """The plugin name

        Returns:
            The name
        """
        return "mock"

    def activate(self, data: dict[str, Any]) -> None:
        configuration = MockGeneratorConfiguration(**data)

        root = self.core_data.project_data.pyproject_file.parent

        modified_file = configuration.test_file_requirement

        if not modified_file.is_absolute():
            modified_file = root / modified_file

        MockGeneratorData(test_file_requirement=modified_file)

    @staticmethod
    def is_supported(path: Path) -> bool:
        """Queries generator support of the given path

        Args:
            path: Input path

        Returns:
            True if supported
        """
        return True

    def sync(self, results: list[SyncData]) -> None:
        pass
