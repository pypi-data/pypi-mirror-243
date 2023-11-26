import json
import pickle
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from environment_backups.exceptions import UploadError


class GDrive:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, secrets_file: Path):
        self.secrets_file = secrets_file
        token_file = secrets_file.parent / 'token.pickle'
        creds = self.get_g_drive_credentials(token_file)
        self.service = build('drive', 'v3', credentials=creds)

    def get_g_drive_credentials(self, token_file):
        creds = None
        # The file token.pickle stores the
        # user's access and refresh tokens. It is
        # created automatically when the authorization
        # flow completes for the first time.
        # Check if file token.pickle exists
        if token_file.exists():
            # Read the token from the file and
            # store it in the variable creds
            # TODO test for age of token. If token is older than 2 weeks?? don't load it.
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        # If no valid credentials are available,
        # request the user to log in.
        if not creds or not creds.valid:

            # If token is expired, it will be refreshed,
            # else, we will request a new one.
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(self.secrets_file), self.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle
            # file for future usage
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def upload(self, file_to_upload: Path, folder_id: str):
        filename = file_to_upload.name
        mime_type = 'application/octet-stream'
        body = {'name': filename, 'parents': [folder_id], 'mimeType': mime_type}
        try:
            media_body = MediaFileUpload(file_to_upload, mimetype=mime_type, chunksize=10485760, resumable=True)
            request = self.service.files().create(body=body, media_body=media_body)  # Modified
            result = request.execute()
            return result
        except Exception as e:
            error_message = f'Upload error. Type {e.__class__.__name__} error {e}'
            raise UploadError(error_message)

    def upload_folder(self, folder_to_upload: Path, parent_folder_id: str):
        """
        Uploads the content of a folder to Google Drive.

        :param folder_to_upload: Path of the folder to upload.
        :param parent_folder_id: ID of the Google Drive folder where the content should be uploaded.
        """
        # Traverse through the folder and its subfolders
        folder_id = self.create_folder(folder_name=folder_to_upload.name, parent_folder_id=parent_folder_id)
        for item in folder_to_upload.iterdir():
            if item.is_dir():
                # If the current item is a subfolder, create a folder in Google Drive and then upload its contents
                folder_id = self.create_folder(item.name, folder_id)
                self.upload_folder(item, folder_id)
            else:
                # If the current item is a file, upload it

                self.upload(item, folder_id)

    def create_folder(self, folder_name: str, parent_folder_id: Optional[str] = None) -> str:
        """
        Creates a folder in Google Drive.

        :param folder_name: Name of the folder to create.
        :param parent_folder_id: ID of the parent folder.
        :return: ID of the created folder.
        """
        body = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        if parent_folder_id:
            body['parents'] = [parent_folder_id]
        folder = self.service.files().create(body=body, fields='id').execute()
        return folder.get('id')

    def list_content(self, parent_folder_id: str):
        """
        Lists all the content (files and folders) in a Google Drive folder.

        :param parent_folder_id: ID of the Google Drive folder.
        :return: List of dictionaries containing 'name' and 'id' of each item.
        """
        results = []
        query = f"'{parent_folder_id}' in parents"

        # Fetch files and folders from the Google Drive API
        response = self.service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()

        # Extract the file names and IDs
        items = response.get('files', [])
        for item in items:
            results.append({'name': item.get('name'), 'id': item.get('id')})

        # Handle pagination
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = (
                self.service.files()
                .list(q=query, fields="nextPageToken, files(id, name)", pageToken=page_token)
                .execute()
            )
            items = response.get('files', [])
            for item in items:
                results.append({'name': item.get('name'), 'id': item.get('id')})

        return results


if __name__ == '__main__':
    sec_file = Path(__file__).parent.parent.parent / '.envs' / 'google_drive' / 'client_secrets.json'
    folder_file = sec_file.parent / 'payjoy_google_folders.json'
    with open(folder_file, 'r') as f:
        folders_dict = json.load(f)
    print(sec_file, sec_file.exists())
    # file_to_upload = sec_file.parent.parent.parent / 'README.md'
    # print(file_to_upload, file_to_upload.exists())
    upload_folder_id = folders_dict['circulo_tests']  # Circulo tests
    gdrive = GDrive(secrets_file=sec_file)
    # response = gdrive.upload(file_to_upload, upload_folder_id)
    # folder_to_upload = Path.home() / 'Documents' / 'PycharmProjects_envs' / '20230921_08'
    folder_to_upload = Path.home() / 'Documents' / 'PycharmProjects_envs' / '20230910_09'
    gdrive.upload_folder(folder_to_upload=folder_to_upload, parent_folder_id=upload_folder_id)
    # gdrive.create_folder('Test_folder', upload_folder_id)
    # print(response)
    print('finished uploading')
    content = gdrive.list_content(parent_folder_id=upload_folder_id)
    for c in content:
        print(c)
        print('-' * 50)
    print('FINISHED')
