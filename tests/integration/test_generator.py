"""
Test the integrations related to the internal generator implementation and the 'Generator' interface itself
"""

import pytest

from pytest_cppython.plugin import GeneratorIntegrationTests
from tests.data import TestGenerator, test_pyproject


class TestCMakeGenerator(GeneratorIntegrationTests):
    """
    The tests for our CMake generator
    """

    @pytest.fixture(name="generator")
    def fixture_generator(self) -> TestGenerator:
        """
        Override of the plugin provided generator fixture.

        Returns:
            CMakeGenerator -- The Generator object to use for the CPPython defined tests
        """

        return TestGenerator(test_pyproject)
