"""
Test the integrations related to the internal generator implementation and the 'Generator' interface itself
"""

from typing import Type

import pytest

from pytest_cppython.mock import MockGenerator, MockGeneratorData
from pytest_cppython.plugin import GeneratorIntegrationTests


class TestMockGenerator(GeneratorIntegrationTests[MockGenerator, MockGeneratorData]):
    """
    The tests for our Mock generator
    """

    @pytest.fixture(name="generator_data", scope="session")
    def fixture_generator_data(self) -> MockGeneratorData:
        """
        A required testing hook that allows GeneratorData generation
        """
        return MockGeneratorData()

    @pytest.fixture(name="generator_type", scope="session")
    def fixture_generator_type(self) -> Type[MockGenerator]:
        """
        A required testing hook that allows type generation
        """
        return MockGenerator
