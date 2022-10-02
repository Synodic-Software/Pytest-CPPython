"""Defines variations of configuration data
"""

from pathlib import Path

from cppython_core.plugin_schema.generator import GeneratorConfiguration
from cppython_core.plugin_schema.provider import ProviderConfiguration
from cppython_core.plugin_schema.vcs import VersionControlConfiguration

provider_config_test_list: list[ProviderConfiguration] = [ProviderConfiguration(root_directory=Path("."))]

generator_config_test_list: list[GeneratorConfiguration] = [GeneratorConfiguration(root_directory=Path("."))]

vcs_config_test_list: list[VersionControlConfiguration] = [VersionControlConfiguration(root_directory=Path("."))]
