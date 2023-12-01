import json

import pytest
from freezegun import freeze_time

from environment_backups.config.configuration import ConfigurationManager


class TestConfigurationManager:
    def test_init(self, tmp_config_folder):
        configuration = ConfigurationManager(tmp_config_folder)
        assert not configuration.config_file.exists()

    def test_import_from_json(self, tmp_config_folder, fixtures_folder):
        config_json_file = fixtures_folder / 'app_configuration.json'

        configuration = ConfigurationManager(tmp_config_folder)

        config_data = configuration.import_from_json(config_json_file).get_current()

        assert configuration.config_file.exists()
        assert config_data
        assert config_data['application']
        assert len(config_data['configurations'])


def test_initialization_with_default_path():
    manager = ConfigurationManager()
    assert manager.config_folder.exists()
    assert manager.config_backup_folder.exists()
    assert manager.logs_folder.exists()


def test_save_and_load_configuration(config_manager):
    test_config = {'key': 'value'}
    config_manager.set_configuration(test_config)
    config_manager.save()
    assert config_manager.config_file.exists()

    # Load configuration
    assert config_manager.load_configuration()
    assert config_manager.get_current() == test_config


def test_export_to_json(config_manager, tmp_path):
    test_config = {'key': 'value'}
    config_manager.set_configuration(test_config)
    export_file = tmp_path / "export.json"
    config_manager.export_to_json(export_file)
    with open(export_file, 'r') as f:
        loaded_config = json.load(f)
    assert loaded_config == test_config


def test_import_from_json(config_manager, tmp_path):
    test_config = {'key': 'value'}
    import_file = tmp_path / "import.json"
    with open(import_file, 'w') as f:
        json.dump(test_config, f)

    config_manager.import_from_json(import_file)
    assert config_manager.get_current() == test_config


@freeze_time('2023-11-03 14:15:16')
def test_backup_creation(config_manager):
    # Initial save to create a configuration file
    initial_config = {'initial': 'config'}
    config_manager.set_configuration(initial_config)
    config_manager.save()

    # Modify and save again to trigger backup
    new_config = {'new': 'config'}
    config_manager.set_configuration(new_config)
    config_manager.save()

    backup_file = list(config_manager.config_backup_folder.glob('*.toml'))[0]
    assert backup_file.name == '20231103_141516_configuration.toml'


def test_delete_configuration(config_manager):
    # Create and save a configuration
    config_manager.set_configuration({'key': 'value'})
    config_manager.save()

    # Delete configuration
    backup_path = config_manager.delete()

    assert not config_manager.config_file.exists()  # Check if config file was deleted
    assert backup_path.exists()  # Check if backup was created


def test_error_handling_import_from_json(config_manager, tmp_path):
    # Set an initial configuration
    config_manager.set_configuration({'key': 'value'})

    # Attempt to import from JSON should raise an error
    import_file = tmp_path / "import.json"
    with open(import_file, 'w') as f:
        json.dump({'new_key': 'new_value'}, f)

    with pytest.raises(ConnectionError):
        config_manager.import_from_json(import_file)


def test_set_and_get_configuration(config_manager):
    test_config = {'key': 'value'}
    config_manager.set_configuration(test_config)

    assert config_manager.get_current() == test_config

# More tests can be added as needed to cover other aspects or edge cases.
