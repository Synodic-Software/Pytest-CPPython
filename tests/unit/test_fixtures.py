"""Tests for fixtures"""

from pathlib import Path

from pytest_cppython.fixtures import CPPythonFixtures


class TestFixtures(CPPythonFixtures):
    """Tests for fixtures"""

    def test_pyproject_undefined(self, data_path: Path) -> None:
        """Verifies that the directory data provided by pytest_cppython contains a pyproject.toml file

        Args:
            data_path: The [project's] tests/data directory
        """

        paths = list(data_path.rglob("pyproject.toml"))

        assert len(paths) == 1
