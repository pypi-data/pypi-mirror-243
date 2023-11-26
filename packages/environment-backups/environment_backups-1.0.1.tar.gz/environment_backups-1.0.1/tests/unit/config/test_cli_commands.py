from click.testing import CliRunner

from environment_backups.config.cli_commands import config


def test_init_existing_values(mock_config_manager, tmp_path):
    mock_config_manager.get_current.return_value = {'config': 'value'}
    toml_config_file = tmp_path / 'test_config.toml'
    mock_config_manager.config_file = toml_config_file
    # mocker.patch(
    #     'environment_backups.config.cli_commands.CONFIGURATION_MANAGER.get_current', return_value={'hello': 'world'}
    # )
    runner = CliRunner()
    result = runner.invoke(config, ['init'])
    output_lines = result.output.split('\n')

    expected_lines = [
        f"Init configuration file: {toml_config_file}",
        "Configuration already exists.",
        ""
    ]

    assert len(output_lines) == 3
    for i, line in enumerate(output_lines):
        assert line == expected_lines[i]

    assert result.exit_code == 100


def test_init_command(mock_config_manager, tmp_path):
    mock_config_manager.get_current.return_value = {}
    runner = CliRunner()
    mock_inputs = '\n'.join(
        ['%Y-%m-%d', '.envs', '', 'my_config_name', str(tmp_path), str(tmp_path), "my_computer_name", 'N', 'N', 'y']
    )
    result = runner.invoke(config, ['init'], input=mock_inputs)

    assert result.exit_code == 0
    assert 'Init configuration file' in result.output
    # Assert if the mock CONFIGURATION_MANAGER was used correctly
    mock_config_manager.set_configuration.assert_called_once()
    if "Yes" in mock_inputs.split('\n'):
        mock_config_manager.save.assert_called_once()


def test_reset_delete(mock_config_manager):
    mock_config_manager.get_current.return_value = {}
    runner = CliRunner()
    mock_inputs = '\n'.join(['Y'])
    result = runner.invoke(config, ['reset'], input=mock_inputs)

    assert result.exit_code == 0
    lines = result.output.split('\n')
    assert len(lines) == 3
    assert 'By resetting the configuration the' in lines[0]
    assert 'Configuration file deleted. A backup was created ' in lines[1]
