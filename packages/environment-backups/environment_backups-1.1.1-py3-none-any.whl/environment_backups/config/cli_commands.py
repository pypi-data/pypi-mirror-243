import sys
from pathlib import Path
from typing import Any, Dict

import click
from rich.pretty import pprint

from environment_backups import CONFIGURATION_MANAGER
from environment_backups.constants import DEFAULT_DATE_FORMAT, DEFAULT_ENV_FOLDER


@click.group()
def config():
    """Configuration entrypoint."""


def custom_control_c_handler(config_dict: Dict[str, Any], signal_numer: int, frame: Any):
    # save = click.confirm('Do you want to save your configuration?')
    # save = input('Save?')
    save = True
    pprint(config_dict)
    if save:
        sys.exit(0)
    else:
        sys.exit(100)


@click.command()
def reset():
    if not CONFIGURATION_MANAGER.config_file.exists():
        click.secho(f'No configuration file found {CONFIGURATION_MANAGER.config_file}', fg='red')
    message = (
        f'By resetting the configuration the {CONFIGURATION_MANAGER.config_file}' f' will be deleted. Are you sure?'
    )
    confirm = click.confirm(message)
    if confirm:
        backup_file = CONFIGURATION_MANAGER.delete()
        click.secho(f'Configuration file deleted. A backup was created {backup_file}', fg='green')


@click.command()
def init():
    click.secho(f'Init configuration file: {CONFIGURATION_MANAGER.config_file}', fg='green')
    if CONFIGURATION_MANAGER.get_current():
        click.secho(f'Configuration already exists.')
        sys.exit(100)

    configuration_dict = {"application": {}, "configurations": []}
    #  signal.signal(signal.SIGINT, partial(custom_control_c_handler, configuration_dict))
    prompt = 'Date format for backup folder prefix'
    configuration_dict['application']['date_format'] = click.prompt(prompt, default=DEFAULT_DATE_FORMAT)

    prompt = 'Environment folder pattern name to parse. If several separate by a comma'
    env_folders = click.prompt(prompt, default=DEFAULT_ENV_FOLDER)
    configuration_dict['application']['environment_folder_pattern'] = [x.strip() for x in env_folders.split(',')]

    prompt = 'Default password for zip files'
    configuration_dict['application']['password'] = click.prompt(prompt, default="")
    keep_adding_configs = True
    while keep_adding_configs:
        c = prompt_for_configuration()
        configuration_dict['configurations'].append(c)
        keep_adding_configs = click.confirm('Do you want to add another configuration?')

    # pprint(configuration_dict)
    CONFIGURATION_MANAGER.set_configuration(configuration_dict)
    save = click.confirm('Save configuration?')

    if save:
        CONFIGURATION_MANAGER.save()


def set_null_if_blank(value: str) -> str | None:
    # FIXME setting the value to None it will not write it to the toml file.
    # print(f'value {value}')
    if len(value) == 0:
        return None
    return value


@click.command()
def edit():
    click.secho(f'Init configuration file: {CONFIGURATION_MANAGER.config_file}', fg='green')
    if not CONFIGURATION_MANAGER.get_current():
        click.secho(f'Configuration is blank run init.', fg='red')
        sys.exit(100)

    configuration_dict = CONFIGURATION_MANAGER.get_current()

    prompt = 'Date format for backup folder prefix'
    configuration_dict['application']['date_format'] = click.prompt(prompt, default=configuration_dict['application'][
        'date_format'])

    prompt = 'Environment folder pattern name to parse. If several separate by a comma'
    patterns = ', '.join(configuration_dict['application']['environment_folder_pattern'])
    env_folders = click.prompt(prompt, default=patterns)
    configuration_dict['application']['environment_folder_pattern'] = [x.strip() for x in env_folders.split(',')]

    prompt = 'Default password for zip files'
    password = configuration_dict['application'].get('password')
    configuration_dict['application']['password'] = click.prompt(prompt,
                                                                 default=password,
                                                                 value_proc=set_null_if_blank)

    for i, env_configuration in enumerate(configuration_dict['configurations']):
        prompt = f'Do you want to edit the configuration for {env_configuration["name"]}'
        edit_env = click.confirm(prompt)
        if edit_env:
            changed_config = prompt_for_configuration(env_configuration)
            configuration_dict['configurations'][i] = changed_config

    CONFIGURATION_MANAGER.set_configuration(configuration_dict)
    save = click.confirm('Save configuration?')

    if save:
        CONFIGURATION_MANAGER.save()


config.add_command(init)
config.add_command(reset)
config.add_command(edit)


# TODO add backup of environment by command environment-backups config backup
# TODO Add restore backup capabilities

# TODO Add support for password at configurations level

def prompt_for_configuration(previous_configuration: Dict[str, Any] = None) -> Dict[str, Any]:
    is_new = False
    if previous_configuration is None:
        previous_configuration = {}
        is_new = True

    config_dict = {}

    prompt = 'Name of the configuration. Must be unique'
    default_value = previous_configuration.get('name')
    config_dict['name'] = click.prompt(prompt, default=default_value)

    # TODO Allow using ~/PycharmProjects for example
    prompt = 'Project folder'
    default_value = previous_configuration.get('projects_folder')
    config_dict['project_folder'] = click.prompt(prompt, type=click.Path(exists=True), default=default_value)

    prompt = 'Backup folder'
    default_value = previous_configuration.get('backup_folder')
    config_dict['backup_folder'] = click.prompt(prompt, type=click.Path(exists=False), default=default_value)

    prompt = 'Computer name'
    # TODO Get computer name from hostname??
    default_value = previous_configuration.get('computer_name')
    config_dict['computer_name'] = click.prompt(prompt, default=default_value)

    if is_new:
        prompt = 'Google drive support?'
        google_drive_support = click.confirm(prompt, default=default_value)
    else:
        google_drive_support = previous_configuration.get('google_drive_folder_id') or previous_configuration.get(
            'google_authentication_file')

    if google_drive_support:
        prompt = 'Google drive folder id'
        default_value = previous_configuration.get('google_drive_folder_id')
        config_dict['google_drive_folder_id'] = click.prompt(prompt, default=default_value)

        prompt = 'Google authentication file'
        default_value = previous_configuration.get('google_authentication_file')
        config_dict['google_authentication_file'] = click.prompt(prompt, type=click.Path(exists=False),
                                                                 default=default_value)

    return config_dict
