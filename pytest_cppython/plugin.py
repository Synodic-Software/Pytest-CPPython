"""
TODO
"""

from typing import Type

from cppython.project import Project as CPPythonProject
from cppython.schema import GeneratorDataType, Interface, PyProject
from pdm import Core, Project
from pdm.models.candidates import Candidate
from pdm.signals import post_install


class CPPythonPlugin(Interface):
    """
    TODO
    """

    def __init__(self, core: Core) -> None:

        self.core = core
        post_install.connect(self.on_post_install)

    def read_generator_data(self, generator_data_type: Type[GeneratorDataType]) -> GeneratorDataType:
        return generator_data_type()

    def write_pyproject(self) -> None:
        """
        TODO:
        """

        pass

    def on_post_install(self, project: Project, candidates: dict[str, Candidate], dry_run: bool):
        """
        TODO
        """

        pyproject = PyProject(**project.config)
        cppython_project = CPPythonProject(self, pyproject)

        cppython_project.install()

    def print(self, string: str) -> None:
        print(string)
