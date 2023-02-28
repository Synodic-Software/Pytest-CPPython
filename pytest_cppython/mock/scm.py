"""Mock SCM definitions"""

from pathlib import Path

from cppython_core.plugin_schema.scm import SCM
from cppython_core.schema import Information


class MockSCM(SCM):
    """A mock generator class for behavior testing"""

    @staticmethod
    def supported(directory: Path) -> bool:
        """_summary_

        Args:
            directory: _description_

        Returns:
            _description_
        """
        return False

    @staticmethod
    def information() -> Information:
        """Returns plugin information

        Returns:
            The plugin information
        """
        return Information()

    def version(self, path: Path) -> str:
        """Extracts the system's version metadata

        Args:
            path: The repository path

        Returns:
            A version
        """
        return "1.0.0"
