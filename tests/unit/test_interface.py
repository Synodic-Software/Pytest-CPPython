"""
TODO
"""

import pytest
from cppython.plugins.test.pytest import InterfaceUnitTests
from pdm import Core
from pytest_mock import MockerFixture

from cppython_pdm.plugin import CPPythonPlugin


class TestCPPythonInterface(InterfaceUnitTests):
    """
    The tests for the PDM interface
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self) -> CPPythonPlugin:
        """
        Override of the plugin provided interface fixture.

        Returns:
            ConsoleInterface -- The Interface object to use for the CPPython defined tests
        """

        return CPPythonPlugin(Core())

    def test_install(self, interface: CPPythonPlugin, mocker: MockerFixture):
        """
        TODO
        """
