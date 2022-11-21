"""Mock interface definitions"""

from cppython_core.plugin_schema.interface import Interface


class MockInterface(Interface):
    """A mock interface class for behavior testing"""

    def write_pyproject(self) -> None:
        """Implementation of Interface function"""
