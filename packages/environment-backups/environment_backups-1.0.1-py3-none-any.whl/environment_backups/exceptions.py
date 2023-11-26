class EnvironmentBackupsError(Exception):
    pass


class UploadError(EnvironmentBackupsError):
    pass


class ConfigurationError(Exception):
    pass
