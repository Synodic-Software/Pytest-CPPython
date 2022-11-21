"""Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

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

    def test_plugin_registration(self, plugin_type: type[MockInterface]) -> None:
        """Override the base class 'ProviderIntegrationTests' preventing a registration check for the Mock

        Args:
            plugin_type: Required to override base function
        """
