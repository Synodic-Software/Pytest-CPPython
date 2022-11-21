"""Tests the integration test plugin
"""

from typing import Any

import pytest

from pytest_cppython.mock.vcs import MockVersionControl
from pytest_cppython.plugin import VersionControlIntegrationTests


class TestCPPythonVersionControl(VersionControlIntegrationTests[MockVersionControl]):
    """The tests for the Mock version control"""

    @pytest.fixture(name="plugin_data", scope="session")
    def fixture_plugin_data(self) -> dict[str, Any]:
        """Returns mock data

        Returns:
            An overridden data instance
        """

        return {}

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[MockVersionControl]:
        """A required testing hook that allows type generation

        Returns:
            An overridden version control type
        """
        return MockVersionControl

    def test_plugin_registration(self, plugin_type: type[MockVersionControl]) -> None:
        """Override the base class 'ProviderIntegrationTests' preventing a registration check for the Mock

        Args:
            plugin_type: Required to override base function
        """
