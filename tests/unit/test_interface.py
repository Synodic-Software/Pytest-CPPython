"""
TODO
"""

import pytest
from cppython_core.schema import InterfaceConfiguration

from pytest_cppython.plugin import InterfaceUnitTests
from tests.data import MockInterface


class TestCPPythonInterface(InterfaceUnitTests[MockInterface]):
    """
    The tests for the PDM interface
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self) -> MockInterface:
        """
        Override of the plugin provided interface fixture.

        Returns:
            ConsoleInterface -- The Interface object to use for the CPPython defined tests
        """
        configuration = InterfaceConfiguration()
        return MockInterface(configuration)
