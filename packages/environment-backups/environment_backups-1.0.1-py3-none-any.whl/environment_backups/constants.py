from environment_backups import CONFIGURATION_MANAGER

DEFAULT_ENV_FOLDER = '.envs'
DEFAULT_DATE_FORMAT = '%Y%m%d_%H'

LOG_FILE = CONFIGURATION_MANAGER.logs_folder / f'{CONFIGURATION_MANAGER.APP_NAME}.log'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": str(LOG_FILE),
            "maxBytes": 1024,
            "backupCount": 3
        }
    },
    "loggers": {
        'environment_backups': {
            "level": "DEBUG",
            "handlers": ['console', 'file'],
            "propagate": False
        },
    },
    "root": {"level": "INFO", "handlers": ["console", ]},
}
