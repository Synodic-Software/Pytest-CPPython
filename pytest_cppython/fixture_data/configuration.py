"""Defines variations of Interface/Provider data
"""

from pathlib import Path

from cppython_core.schema import ProviderConfiguration

provider_config_test_list: list[ProviderConfiguration] = [ProviderConfiguration(root_directory=Path("."))]
