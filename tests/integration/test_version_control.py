"""Tests the integration test plugin
"""

import pytest

from pytest_cppython.mock import MockVersionControl, MockVersionControlData
from pytest_cppython.plugin import VersionControlIntegrationTests


class TestCPPythonVersionControl(VersionControlIntegrationTests[MockVersionControl, MockVersionControlData]):
    """The tests for the Mock version control"""

    @pytest.fixture(name="plugin_data", scope="session")
    def fixture_plugin_data(self) -> MockVersionControlData:
        """A required testing hook that allows VersionControl generation

        Returns:
            An overridden data instance
        """
        return MockVersionControlData()

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_version_control_type(self) -> type[MockVersionControl]:
        """A required testing hook that allows type generation

        Returns:
            An overridden version control type
        """
        return MockVersionControl
