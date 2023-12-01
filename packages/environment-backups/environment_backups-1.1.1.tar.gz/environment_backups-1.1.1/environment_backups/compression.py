import os
from pathlib import Path

from pyzipper import WZ_AES, AESZipFile, ZIP_DEFLATED

from environment_backups.exceptions import EnvironmentBackupsError


def zip_folder_with_pwd(zip_file: Path, folder_to_zip: Path, password: str = None):
    """
    Compresses a folder and creates a zip file with optional password protection.
    @param zip_file:
    @param folder_to_zip:
    @param password:
    """
    if not folder_to_zip.exists():
        message = f'The target folder to put the zip file {folder_to_zip}does not exist.'
        raise EnvironmentBackupsError(message)

    def zipdir(path: Path, ziph):
        """
        Recursively adds files and directories to a zip file.
        """

        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                ziph.write(file_path, os.path.relpath(file_path, path.parent))

    encryption = WZ_AES if password else None

    with AESZipFile(zip_file, 'w', compression=ZIP_DEFLATED, encryption=encryption) as zf:
        if password:
            pwd = password.encode('utf-8')
            zf.setpassword(pwd)
        zipdir(folder_to_zip, zf)
