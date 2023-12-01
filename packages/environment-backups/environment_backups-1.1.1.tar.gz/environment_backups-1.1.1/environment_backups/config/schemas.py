from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field

from environment_backups.constants import DEFAULT_DATE_FORMAT


class Application(BaseModel):
    environment_folder_pattern: List[str] = Field(default=['.envs'])
    date_format: str = Field(default=DEFAULT_DATE_FORMAT)
    password: str = Field(default=None)


class Configuration(BaseModel):
    name: str = Field(description='Unique name for configuration')
    projects_folder: Path
    backup_folder: Path
    computer_name: str
    google_drive_folder_id: Optional[str] = None
    google_authentication_file: Optional[Path] = None


class ApplicationConfiguration(BaseModel):
    application: Application
    configurations: List[Configuration]
