from pathlib import Path

import pytest
from freezegun import freeze_time

from environment_backups.backups.backups import (list_all_projects, get_projects_envs, zip_folder_with_pwd,
                                                 backup_envs, backup_environment)
from environment_backups.exceptions import ConfigurationError


# TODO Fix broken tests

def test_list_all_projects_with_existing_folders(mocker):
    # Mock os.scandir to return a list of mock directories
    mocker.patch('os.scandir', return_value=[mocker.Mock(is_dir=lambda: True, path='dir1'),
                                             mocker.Mock(is_dir=lambda: True, path='dir2')])
    assert list_all_projects(Path('/some/path')) == ['dir1', 'dir2']


def test_list_all_projects_with_no_folders(mocker):
    # Mock os.scandir to return an empty list
    mocker.patch('os.scandir', return_value=[])
    assert list_all_projects(Path('/some/empty/path')) == []


def test_get_projects_envs_with_valid_data(mocker):
    # Mock list_all_projects to return specific folders
    mocker.patch('environment_backups.backups.backups.list_all_projects', return_value=['project1', 'project2'])
    # Mock Path.exists to return True
    mocker.patch('pathlib.Path.exists', return_value=True)
    expected_result = {
        'project1': {'envs': Path('project1/env_folder')},
        'project2': {'envs': Path('project2/env_folder')}
    }
    assert get_projects_envs(Path('/projects'), ['env_folder']) == expected_result


def test_get_projects_envs_with_no_projects(mocker):
    mocker.patch('environment_backups.backups.backups.list_all_projects', return_value=[])
    assert get_projects_envs(Path('/projects'), ['env_folder']) == {}


def test_zip_folder_with_pwd_without_password(mocker, tmp_path):
    # Set up a temporary directory and files for zipping
    folder_to_zip = tmp_path / "test_folder"
    folder_to_zip.mkdir()
    (folder_to_zip / "test_file.txt").write_text("test content")

    zip_file = tmp_path / "test.zip"

    # Call the function
    zip_folder_with_pwd(zip_file, folder_to_zip)

    # Check if the zip file was created
    assert zip_file.exists()


def test_zip_folder_with_pwd_with_password(mocker, tmp_path):
    # Similar setup as above, but pass a password to the function
    folder_to_zip = tmp_path / "test_folder"
    folder_to_zip.mkdir()
    (folder_to_zip / "test_file.txt").write_text("test content")

    zip_file = tmp_path / "test.zip"

    zip_folder_with_pwd(zip_file, folder_to_zip, password="secret")

    assert zip_file.exists()


def test_zip_folder_with_empty_directory(mocker, tmp_path):
    # Test with an empty directory
    folder_to_zip = tmp_path / "empty_folder"
    folder_to_zip.mkdir()

    zip_file = tmp_path / "empty.zip"

    zip_folder_with_pwd(zip_file, folder_to_zip)

    assert zip_file.exists()


@freeze_time("2023-11-02 13:16:12")
def test_backup_envs_with_valid_data(mocker, tmp_path):
    # Mock get_projects_envs to return a dictionary of projects with environments
    mocker.patch(
        'environment_backups.backups.backups.get_projects_envs',
        return_value={'project1': {'envs': Path('/envs/project1')}}
    )

    # Mock os.path.exists and Path.mkdir
    mocker.patch.object(Path, 'exists', return_value=True)
    mocker.patch.object(Path, 'mkdir')

    expected_timestamp = '20231102_13'

    # Paths for projects folder and backup folder
    projects_folder = Path('/projects')
    backup_folder = tmp_path / 'backups'

    # Call the function
    zip_list, b_folder = backup_envs(
        projects_folder=projects_folder,
        backup_folder=backup_folder,
        environment_folders=['env1', 'env2'],
        password='password'
    )

    # Assertions
    assert len(zip_list) == 1
    assert b_folder == backup_folder / expected_timestamp
    assert zip_list[0] == backup_folder / expected_timestamp / 'project1.zip'


def test_backup_environments_with_valid_configuration(mocker, tmp_path):
    # Mock CONFIGURATION_MANAGER and get_configuration_by_name
    mocker.patch(
        'your_module.CONFIGURATION_MANAGER.get_current',
        return_value={'password': 'password', 'env_folder_pattern': ['env'], 'date_format': '%Y%m%d_%H'}
    )
    mocker.patch(
        'your_module.get_configuration_by_name',
        return_value=({'project_folder': '/projects', 'backup_folder': str(tmp_path / 'backups')}, None)
    )

    # Mock backup_envs
    mocker.patch(
        'your_module.backup_envs',
        return_value=([Path('/backups/backup.zip')], tmp_path / 'backups')
    )

    # Call the function
    zip_list, b_folder = backup_environment('test_env')

    # Assertions
    assert len(zip_list) == 1
    assert zip_list[0] == Path('/backups/backup.zip')
    assert b_folder == tmp_path / 'backups'


def test_backup_environments_with_invalid_configuration(mocker):
    # Mock CONFIGURATION_MANAGER and get_configuration_by_name to return None
    mocker.patch(
        'your_module.CONFIGURATION_MANAGER.get_current',
        return_value={'password': '', 'env_folder_pattern': ['env'], 'date_format': '%Y%m%d_%H'}
    )
    mocker.patch(
        'your_module.get_configuration_by_name',
        return_value=(None, None)
    )

    # Test with an invalid configuration to raise ConfigurationError
    with pytest.raises(ConfigurationError) as excinfo:
        backup_environments('invalid_env')
    assert 'No environment configuration found for "invalid_env"' in str(excinfo.value)
