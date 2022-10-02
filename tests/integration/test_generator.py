"""Tests the integration test plugin
"""

import pytest

from pytest_cppython.mock import MockGenerator, MockGeneratorData
from pytest_cppython.plugin import GeneratorIntegrationTests


class TestCPPythonGenerator(GeneratorIntegrationTests[MockGenerator, MockGeneratorData]):
    """The tests for the Mock generator"""

    @pytest.fixture(name="plugin_data", scope="session")
    def fixture_plugin_data(self) -> MockGeneratorData:
        """A required testing hook that allows GeneratorData generation

        Returns:
            An overridden data instance
        """
        return MockGeneratorData()

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[MockGenerator]:
        """A required testing hook that allows type generation

        Returns:
            An overridden generator type
        """
        return MockGenerator
