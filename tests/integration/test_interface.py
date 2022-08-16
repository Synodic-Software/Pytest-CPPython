"""
Tests the integration test plugin
"""

from typing import Type

import pytest

from pytest_cppython.mock import MockInterface
from pytest_cppython.plugin import InterfaceIntegrationTests


class TestCPPythonInterface(InterfaceIntegrationTests[MockInterface]):
    """
    The tests for the PDM interface
    """

    @pytest.fixture(name="interface_type")
    def fixture_interface_type(self) -> Type[MockInterface]:
        """
        A required testing hook that allows type generation
        """
        return MockInterface
