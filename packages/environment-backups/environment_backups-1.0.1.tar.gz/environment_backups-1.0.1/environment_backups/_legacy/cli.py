import argparse
from pathlib import Path

from environment_backups._legacy.pretty_print import TerminalColor, print_color, print_error, print_success
from environment_backups.backups.backups import backup_envs

COMMANDS = ['backup', 'list']


def main_arg_parser():
    """Main function to backup environment folders using ArgumentParser and regular print statements."""
    parsed_args = parse_arguments()
    if parsed_args.command == 'backup':
        zip_files, ts_backup_folder = backup_envs(
            projects_folder=parsed_args.folder,
            backup_folder=parsed_args.target_folder,
            environment_folders=parsed_args.environment_folder,
        )
        for i, zf in enumerate(zip_files, 1):
            file_size = zf.stat().st_size / 1024
            print_success(f'{i} {zf.name:40} size: {file_size:,.3f} KB')

        print_color(f'Wrote {len(zip_files)} zip files', color=TerminalColor.OK_CYAN)
        if parsed_args.password:
            print_error(f'Zipped files with password: "{parsed_args.password}"')
        print_color(f'Output folder: {ts_backup_folder}', color=TerminalColor.OK_CYAN)
    elif parsed_args.command == 'list':
        print_error('Not supported yet')


def parse_arguments():
    parser = argparse.ArgumentParser(description="Environment backups")
    parser.add_argument(
        "command", type=str, choices=COMMANDS, help=f"Command to execute. Values: {', '.join(COMMANDS)}"
    )
    parser.add_argument(
        "-e",
        "--environment-folder",
        type=str,
        nargs="+",
        help="Name of the environment folder to backup",
        default=['.envs'],
    )
    parser.add_argument("-f", "--folder", type=Path, help="Folder where the projects are found.", required=False)
    parser.add_argument("-t", "--target-folder", type=Path, help="Folder to save the zipped files.", required=False)
    parser.add_argument("-p", "--password", type=str, help="Password for the zip files.", required=False)
    parsed_args = parser.parse_args()
    return parsed_args
