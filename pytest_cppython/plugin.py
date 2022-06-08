"""
Helper fixtures and plugin definitions for pytest
"""
from abc import ABC
from importlib.metadata import entry_points
from pathlib import Path
from typing import Generic

import pytest
from cppython_core.schema import GeneratorT, InterfaceT


class GeneratorTests(ABC, Generic[GeneratorT]):
    """
    Shared functionality between the different Generator testing categories
    """

    @pytest.fixture(name="generator")
    def fixture_generator(self) -> GeneratorT:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("generator", [CustomGenerator])
        """
        raise NotImplementedError


class GeneratorIntegrationTests(GeneratorTests[GeneratorT]):
    """
    Base class for all generator integration tests that test plugin agnostic behavior
    """

    def test_plugin_registration(self, generator: GeneratorT):
        """
        Test the registration with setuptools entry_points
        """
        plugin_entries = entry_points(group=f"cppython.{generator.group()}")
        assert len(plugin_entries) > 0

    def test_is_downloaded(self, generator: GeneratorT, tmp_path: Path):
        """
        TODO
        """

        assert not generator.generator_downloaded(tmp_path)

        generator.download_generator(tmp_path)

        assert generator.generator_downloaded(tmp_path)


class GeneratorUnitTests(GeneratorTests[GeneratorT]):
    """
    Custom implementations of the Generator class should inherit from this class for its tests.
    Base class for all generator unit tests that test plugin agnostic behavior
    """

    def test_name(self, generator: GeneratorT):
        """
        Test name restrictions
        TODO: This should be a pydantic schema
        """
        name = generator.name()

        assert name != ""

    def test_data_type(self, generator: GeneratorT):
        """
        Test data_type restrictions
        TODO: This should be a pydantic schema
        """
        data_type = generator.data_type()

        assert data_type != ""

    def test_preset_generation(self, generator: GeneratorT):
        """
        Tests the generation of the cmake configuration preset
        """
        generator.generate_cmake_config()


class InterfaceTests(ABC, Generic[InterfaceT]):
    """
    Shared functionality between the different Interface testing categories
    """

    @pytest.fixture(name="interface")
    def fixture_interface(self) -> InterfaceT:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("interface", [CustomInterface])
        """
        raise NotImplementedError


class InterfaceIntegrationTests(InterfaceTests[InterfaceT]):
    """
    Base class for all interface integration tests that test plugin agnostic behavior
    """


class InterfaceUnitTests(InterfaceTests[InterfaceT]):
    """
    Custom implementations of the Interface class should inherit from this class for its tests.
    Base class for all interface unit tests that test plugin agnostic behavior
    """

    def test_name(self, interface: InterfaceT):
        """
        Test name restrictions
        TODO: This should be a pydantic schema
        """
        name = interface.name()

        assert name != ""
