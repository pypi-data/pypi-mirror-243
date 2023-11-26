import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import toml

from .utils import backup_file


class ConfigurationManager:
    DEFAULT_CONFIG_FOLDER_NAME = '.environment_backups'
    DEFAULT_CONFIG_FILENAME = 'configuration.toml'
    APP_NAME = DEFAULT_CONFIG_FOLDER_NAME[1:].replace('_', '-')

    def __init__(self, config_root_folder: Optional[Path] = None, config_filename: Optional[str] = None):
        # TODO Add version to init for use in backups

        if config_root_folder is None:
            self.config_folder = Path().home() / self.DEFAULT_CONFIG_FOLDER_NAME
        else:
            self.config_folder = config_root_folder / self.DEFAULT_CONFIG_FOLDER_NAME

        if config_filename is None:
            self.config_file = self.config_folder / self.DEFAULT_CONFIG_FILENAME
        else:
            self.config_file = self.config_folder / config_filename

        self.config_backup_folder = self.config_folder / 'backups'
        self.logs_folder = self.config_folder / 'logs'

        self.username = os.getlogin()
        self.prep_config()
        self.configuration = {}
        self.load_configuration()

    def prep_config(self):
        self.config_folder.mkdir(exist_ok=True)
        self.config_backup_folder.mkdir(exist_ok=True)
        self.logs_folder.mkdir(exist_ok=True)

    def save(self) -> None:
        if self.config_file.exists():
            self.backup()
        with open(self.config_file, 'w') as f:
            toml.dump(self.configuration, f)

    def load_configuration(self) -> bool:
        if not self.config_file.exists():
            return False
        with open(self.config_file, 'r') as f:
            self.configuration = toml.load(f)
        return True

    def export_to_json(self, export_file: Path) -> None:
        with open(export_file, 'w') as f:
            json.dump(self.configuration, f)

    def import_from_json(self, import_file: Path) -> Any:
        if self.configuration:
            raise ConnectionError('There is a configuration already loaded.')
        with open(import_file, 'r') as f:
            self.configuration = json.load(f)
        self.save()
        return self

    def backup(self) -> Path:
        if self.config_file.exists():
            # TODO Add version number
            backup_filename = backup_file(self.config_file, self.config_backup_folder)
            return backup_filename

    def delete(self) -> Path:
        backup_filename: Path = self.backup()
        self.config_file.unlink(missing_ok=True)
        return backup_filename

    def get_current(self):
        return self.configuration

    def set_configuration(self, configuration: Dict[str, Any]) -> Any:
        self.backup()
        self.configuration = configuration
        return self


def get_configuration_by_name(
    config_name: str, app_configuration: Dict[str, Any]
) -> Tuple[Dict[str, Any] | None, float]:
    """Get the configuration based on a name.
    @param config_name: Name of the configuration.
    @param app_configuration: Application configuration.
    @return: Tuple with configuration and fuzzy probabilliy
    """
    # TODO Implement thefuzz for fuzzy search
    config = None
    configurations = app_configuration.get('configurations', [])
    if len(configurations) == 0:
        return None, 100.0
    for configuration in configurations:
        if configuration['name'] == config_name:
            config = configuration

    return config, 100.0
