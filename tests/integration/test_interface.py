"""
TODO
"""
import pytest

from pytest_cppython.plugin import InterfaceIntegrationTests
from tests.data import TestInterface


class TestCPPythonInterface(InterfaceIntegrationTests):
    """
    The tests for the PDM interface
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self) -> TestInterface:
        """
        Override of the plugin provided interface fixture.

        Returns:
            ConsoleInterface -- The Interface object to use for the CPPython defined tests
        """
        return TestInterface()
