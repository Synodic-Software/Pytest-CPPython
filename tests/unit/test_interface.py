"""
Test the functions related to the internal interface implementation and the 'Interface' interface itself
"""

from typing import Type

import pytest

from pytest_cppython.mock import MockInterface
from pytest_cppython.plugin import InterfaceUnitTests


class TestCPPythonInterface(InterfaceUnitTests[MockInterface]):
    """
    The tests for the PDM interface
    """

    @pytest.fixture(name="interface_type")
    def fixture_interface_type(self) -> Type[MockInterface]:
        """
        A required testing hook that allows type generation
        """
        return MockInterface
