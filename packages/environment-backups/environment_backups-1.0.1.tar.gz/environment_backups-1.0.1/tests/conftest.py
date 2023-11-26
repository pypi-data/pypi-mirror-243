import shutil
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from environment_backups import ConfigurationManager


@pytest.fixture(scope='session')
def output_folder() -> Path:
    folder = Path(__file__).parent.parent / 'output'
    return folder


@pytest.fixture(scope='session')
def tmp_config_folder(output_folder) -> Path:
    c_folder = output_folder / 'tmp_config_folder'
    c_folder.mkdir()
    yield c_folder
    shutil.rmtree(c_folder)


@pytest.fixture(scope='session')
def fixtures_folder() -> Path:
    folder = Path(__file__).parent / 'fixtures'
    return folder


@pytest.fixture
def config_manager(tmp_path) -> ConfigurationManager:
    return ConfigurationManager(config_root_folder=tmp_path)


@pytest.fixture
def mock_config_manager(mocker):
    # Create a MagicMock object to mock CONFIGURATION_MANAGER
    mock_manager = MagicMock()
    # Replace CONFIGURATION_MANAGER with the mock object
    mocker.patch('environment_backups.config.cli_commands.CONFIGURATION_MANAGER', new=mock_manager)
    return mock_manager
