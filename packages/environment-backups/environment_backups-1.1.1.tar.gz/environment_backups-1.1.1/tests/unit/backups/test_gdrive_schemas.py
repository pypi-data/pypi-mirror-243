from environment_backups.backups.gdrive_schemas import Installed


class TestGoogleConfiguration:
    def test_create_minimal(self):
        installed_app = Installed(
            client_id='555555555555-00000000000000000000000000000000.apps.googleusercontent.com',
            project_id='my-new-project',
            client_secret='jjjjsdfas',
            redirect_uris=['http://localhost'],
        )
        assert installed_app
