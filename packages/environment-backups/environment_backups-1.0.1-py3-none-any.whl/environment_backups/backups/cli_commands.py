import sys
from pathlib import Path

import click

from environment_backups import CONFIGURATION_MANAGER
from environment_backups.backups.backups import backup_envs, backup_environment
from environment_backups.config.configuration import get_configuration_by_name
from environment_backups.exceptions import EnvironmentBackupsError


@click.command()
@click.option('environment', '-e', '--environment', type=str, required=False)
@click.option('projects_folder', '-p', '--projects-folder', type=click.Path(exists=True), required=False)
@click.option('backup_folder', '-b', '--backup-folder', type=click.Path(exists=False), required=False)
def backup(environment: str, projects_folder: Path, backup_folder: Path):
    if environment:
        app_cfg = CONFIGURATION_MANAGER.get_current()
        env_cfg, _ = get_configuration_by_name(config_name=environment, app_configuration=app_cfg)
        if env_cfg is None:
            click.secho(f'No environment configuration found for {environment}.', fg='red')
            sys.exit(100)
        zip_list, b_folder = backup_environment(environment_name=environment)

        for i, zip_file in enumerate(zip_list, 1):
            click.secho(f'{i:3}. {zip_file.name}', fg='green')

    else:
        legacy_backup(backup_folder, projects_folder)


def legacy_backup(backup_folder, projects_folder):
    if projects_folder is None:
        raise EnvironmentBackupsError('Missing projects folder')
    else:
        projects_folder = Path(projects_folder)
    if backup_folder is None:
        raise EnvironmentBackupsError('Missing backup folder')
    else:
        backup_folder = Path(backup_folder)
    environment_folders = ['.envs']
    zip_list, b_folder = backup_envs(
        projects_folder=projects_folder, backup_folder=backup_folder, environment_folders=environment_folders
    )
    for i, zip_file in enumerate(zip_list, 1):
        click.secho(f'{i:3}. {zip_file.name}', fg='green')

# TODO add backup by name. environment-backups backup --name adelantos --upload
# TODO Upload to google after excectuting a backup.
