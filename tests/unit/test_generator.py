"""
Test the functions related to the internal generator implementation and the 'Generator' interface itself
"""

import pytest

from pytest_cppython.plugin import GeneratorUnitTests
from tests.data import MockGenerator, test_configuration, test_pyproject


class TestCMakeGenerator(GeneratorUnitTests):
    """
    The tests for our CMake generator
    """

    @pytest.fixture(name="generator")
    def fixture_generator(self) -> MockGenerator:
        """
        Override of the plugin provided generator fixture.

        Returns:
            CMakeGenerator -- The Generator object to use for the CPPython defined tests
        """
        return MockGenerator(test_configuration, test_pyproject)
