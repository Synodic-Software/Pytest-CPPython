"""Test the integrations related to the internal provider implementation and the 'Provider' interface itself
"""

from importlib.metadata import EntryPoint
from typing import Any

import pytest

from pytest_cppython.mock.provider import MockProvider
from pytest_cppython.plugin import ProviderIntegrationTests


class TestMockProvider(ProviderIntegrationTests[MockProvider]):
    """The tests for our Mock provider"""

    @pytest.fixture(name="plugin_data", scope="session")
    def fixture_plugin_data(self) -> dict[str, Any]:
        """Returns mock data

        Returns:
            An overridden data instance
        """

        return {}

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[MockProvider]:
        """A required testing hook that allows type generation

        Returns:
            The overridden provider type
        """
        return MockProvider

    @pytest.fixture(name="entry_point", scope="session")
    def fixture_entry_point(self, plugin_type: type[MockProvider]) -> EntryPoint:
        """Override the entry point for the mock object

        Args:
            plugin_type: A plugin type

        Return:
            The entry point definition
        """

        return EntryPoint(
            name=f"{plugin_type.name()}",
            value="pytest_cppython.mock.provider:MockProvider",
            group=f"cppython.{plugin_type.group()}",
        )
