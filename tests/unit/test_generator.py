"""
Test the functions related to the internal generator implementation and the 'Generator' interface itself
"""

from typing import Type

import pytest

from pytest_cppython.mock import MockGenerator, MockGeneratorData
from pytest_cppython.plugin import GeneratorUnitTests


class TestMockGenerator(GeneratorUnitTests[MockGenerator, MockGeneratorData]):
    """
    The tests for our Mock generator
    """

    @pytest.fixture(name="generator_data")
    def fixture_generator_data(self) -> MockGeneratorData:
        """
        A required testing hook that allows GeneratorData generation
        """
        return MockGeneratorData()

    @pytest.fixture(name="generator_type")
    def fixture_generator_type(self) -> Type[MockGenerator]:
        """
        A required testing hook that allows type generation
        """
        return MockGenerator
