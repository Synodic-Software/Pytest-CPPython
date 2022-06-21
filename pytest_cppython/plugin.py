"""
Helper fixtures and plugin definitions for pytest
"""
from abc import ABC
from importlib.metadata import entry_points
from pathlib import Path
from typing import Generic, Type

import pytest
from cppython_core.schema import (
    PEP621,
    CPPythonData,
    GeneratorConfiguration,
    GeneratorDataT,
    GeneratorT,
    InterfaceConfiguration,
    InterfaceT,
)

from pytest_cppython.fixtures import CPPythonFixtures


class GeneratorTests(ABC, CPPythonFixtures, Generic[GeneratorT, GeneratorDataT]):
    """
    Shared functionality between the different Generator testing categories
    """

    @pytest.fixture(name="generator_data")
    def fixture_generator_data(self) -> GeneratorDataT:
        """
        A required testing hook that allows GeneratorData generation
        """
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="generator_type")
    def fixture_generator_type(self) -> Type[GeneratorT]:
        """
        A required testing hook that allows type generation
        """
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="generator")
    def fixture_generator(
        self,
        generator_type: Type[GeneratorT],
        generator_configuration: GeneratorConfiguration,
        pep621: PEP621,
        cppython: CPPythonData,
        generator_data: GeneratorDataT,
    ) -> GeneratorT:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("generator", [CustomGenerator])
        """
        return generator_type(generator_configuration, pep621, cppython, generator_data)


class GeneratorIntegrationTests(GeneratorTests[GeneratorT, GeneratorDataT]):
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

    def test_install(self):
        """
        TODO
        """


class GeneratorUnitTests(GeneratorTests[GeneratorT, GeneratorDataT]):
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


class InterfaceTests(ABC, CPPythonFixtures, Generic[InterfaceT]):
    """
    Shared functionality between the different Interface testing categories
    """

    @pytest.fixture(name="interface_type")
    def fixture_generator_type(self) -> Type[InterfaceT]:
        """
        A required testing hook that allows type generation
        """
        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="interface")
    def fixture_interface(
        self, interface_type: Type[InterfaceT], interface_configuration: InterfaceConfiguration
    ) -> InterfaceT:
        """
        A hook allowing implementations to override the fixture with a parameterization
            @pytest.mark.parametrize("interface", [CustomInterface])
        """
        return interface_type(interface_configuration)


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
