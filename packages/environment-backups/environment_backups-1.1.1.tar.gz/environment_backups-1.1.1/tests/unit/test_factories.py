import shutil

from environment_backups.constants import DEFAULT_DATE_FORMAT
from tests.factories import projects_folder_tree_factory, configuration_factory


def test_create_projects_folder(tmp_path):
    root_folder = tmp_path  # Path(__file__).parent.parent.parent / 'output'
    assert root_folder.exists()
    projects_list = ['project1', 'project2']
    projects_folder, config_files = projects_folder_tree_factory(root_folder=root_folder,
                                                                 projects_folders=projects_list)

    projects_folder = root_folder / 'MyProjectsForTests'
    assert projects_folder.exists()
    for project in projects_list:
        assert (projects_folder / project).exists()

    for config_file in config_files:
        assert config_file.exists()
    shutil.rmtree(projects_folder)


def test_build_valid_configuration_for_tests(tmp_path):
    projects_folder = tmp_path / 'MyProjectsFolder'

    config = configuration_factory(projects_folder=projects_folder)
    assert config.application.date_format == DEFAULT_DATE_FORMAT
    assert config.application.password is None
    assert config.application.environment_folder_pattern == ['.envs']
    assert len(config.configurations) == 1
    assert config.configurations[0].projects_folder.exists()
    assert config.configurations[0].backup_folder.exists()
    assert config.configurations[0].computer_name is not None
    assert config.configurations[0].name is not None
    assert config.configurations[0].google_drive_folder_id is not None
    assert config.configurations[0].google_authentication_file is not None
