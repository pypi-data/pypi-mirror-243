from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from environment_backups.config.cli_commands import edit
from tests.factories import configuration_factory


def test_edit_command_apps_values(tmp_path):
    """
    Test the 'edit' command of the CLI application. Changes for the applications keys

    This test checks the following:
    - The command outputs the initial message with the config file path.
    - The command prompts for inputs and updates the configuration accordingly.
    - The command calls the save method of CONFIGURATION_MANAGER if the user confirms the save.
    """
    # Mock CONFIGURATION_MANAGER
    mock_config_manager = MagicMock()

    projects_folder = tmp_path / 'MyProjects'
    app_configuration = configuration_factory(projects_folder=projects_folder, google_support=False)
    app_configuration_dict = app_configuration.model_dump()
    mock_config_manager.get_current.return_value = app_configuration_dict

    mock_config_manager.config_file = '/path/to/config.toml'

    # Simulate user inputs
    inputs = ['YYYY-MM-DD', 'pattern1, pattern3', 'new_password', 'y', '', '', '', '', 'y']
    mock_inputs = '\n'.join(inputs)

    with patch('environment_backups.config.cli_commands.CONFIGURATION_MANAGER', mock_config_manager):
        runner = CliRunner()
        result = runner.invoke(edit, input=mock_inputs)

    # Assertions
    output_lines = result.output.split('\n')
    expected_lines = [
        "Init configuration file: /path/to/config.toml",
        "Date format for backup folder prefix [%Y%m%d_%H]: YYYY-MM-DD",
        "Environment folder pattern name to parse. If several separate by a comma [.envs]: pattern1, pattern3",
        "Default password for zip files: new_password",
        "Do you want to edit the configuration for test_config_0 [y/N]: y",
        "Name of the configuration. Must be unique [test_config_0]: ",
        f"Project folder [{app_configuration.configurations[0].projects_folder}]: ",
        f"Backup folder [{app_configuration.configurations[0].backup_folder}]: ",
        "Computer name [deep-space9_0]: ",
        "Save configuration? [y/N]: y",
        ""
    ]
    # assert 'Init configuration file: /path/to/config.toml' in result.output
    assert len(output_lines) == 11
    assert result.exit_code == 0
    for i, line in enumerate(output_lines):
        assert line == expected_lines[i]
    mock_config_manager.set_configuration.assert_called_once()
    # TODO assert called one with for set_configuration
    mock_config_manager.save.assert_called_once()

def test_edit_command_change_name(tmp_path):
    """
    Test the 'edit' command of the CLI application.

    This test checks the following:
    - The command outputs the initial message with the config file path.
    - The command prompts for inputs and updates the configuration accordingly.
    - The command calls the save method of CONFIGURATION_MANAGER if the user confirms the save.
    """
    # Mock CONFIGURATION_MANAGER
    mock_config_manager = MagicMock()

    projects_folder = tmp_path / 'MyProjects'
    app_configuration = configuration_factory(projects_folder=projects_folder, google_support=False)
    app_configuration_dict = app_configuration.model_dump()
    mock_config_manager.get_current.return_value = app_configuration_dict

    mock_config_manager.config_file = '/path/to/config.toml'

    # Simulate user inputs
    new_config_name = f'{app_configuration.configurations[0].name}-NEW'
    inputs = ['YYYY-MM-DD', 'pattern1, pattern3', 'new_password', 'y', new_config_name, '', '', '', 'y']
    mock_inputs = '\n'.join(inputs)

    with patch('environment_backups.config.cli_commands.CONFIGURATION_MANAGER', mock_config_manager):
        runner = CliRunner()
        result = runner.invoke(edit, input=mock_inputs)

    # Assertions
    output_lines = result.output.split('\n')
    expected_lines = [
        "Init configuration file: /path/to/config.toml",
        "Date format for backup folder prefix [%Y%m%d_%H]: YYYY-MM-DD",
        "Environment folder pattern name to parse. If several separate by a comma [.envs]: pattern1, pattern3",
        "Default password for zip files: new_password",
        "Do you want to edit the configuration for test_config_0 [y/N]: y",
        f"Name of the configuration. Must be unique [test_config_0]: {new_config_name}",
        f"Project folder [{app_configuration.configurations[0].projects_folder}]: ",
        f"Backup folder [{app_configuration.configurations[0].backup_folder}]: ",
        "Computer name [deep-space9_0]: ",
        "Save configuration? [y/N]: y",
        ""
    ]
    # assert 'Init configuration file: /path/to/config.toml' in result.output
    assert len(output_lines) == 11
    assert result.exit_code == 0
    for i, line in enumerate(output_lines):
        assert line == expected_lines[i]
    mock_config_manager.set_configuration.assert_called_once()
    # TODO assert called one with for set_configuration
    mock_config_manager.save.assert_called_once()

