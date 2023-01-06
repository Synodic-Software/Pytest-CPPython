"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from importlib.metadata import EntryPoint

import pytest

from pytest_cppython.mock.interface import MockInterface
from pytest_cppython.plugin import InterfaceUnitTests


class TestCPPythonInterface(InterfaceUnitTests[MockInterface]):
    """The tests for the Mock interface"""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[MockInterface]:
        """A required testing hook that allows type generation

        Returns:
            An overridden interface type
        """
        return MockInterface

    @pytest.fixture(name="entry_point", scope="session")
    def fixture_entry_point(self, plugin_type: type[MockInterface]) -> EntryPoint:
        """Override the entry point for the mock object

        Args:
            plugin_type: A plugin type

        Return:
            The entry point definition
        """

        return EntryPoint(
            name=f"{plugin_type.name()}",
            value="pytest_cppython.mock.interface:MockInterface",
            group=f"cppython.{plugin_type.group()}",
        )
