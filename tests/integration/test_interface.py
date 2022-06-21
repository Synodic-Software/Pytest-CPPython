"""
TODO
"""
from typing import Type

import pytest

from pytest_cppython.plugin import InterfaceIntegrationTests
from tests.data import MockInterface


class TestCPPythonInterface(InterfaceIntegrationTests[MockInterface]):
    """
    The tests for the PDM interface
    """

    @pytest.fixture(name="interface_type")
    def fixture_generator_type(self) -> Type[MockInterface]:
        """
        A required testing hook that allows type generation
        """
        return MockInterface
