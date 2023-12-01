from __future__ import annotations

import re
from typing import List

from pydantic import AnyHttpUrl, BaseModel, Field, HttpUrl, ValidationError
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated


def validate_client_id(v: str) -> str:
    regexp = re.compile(f"^\w+-\w+.apps.googleusercontent.com$")
    match = regexp.match(v)
    if match:
        return v
    else:
        raise ValidationError(f'The client id does not comply with the expected pattern')


ClientId = Annotated[str, AfterValidator(validate_client_id)]


class Installed(BaseModel):
    client_id: ClientId
    project_id: str
    auth_uri: HttpUrl = Field(default="https://accounts.google.com/o/oauth2/auth")
    token_uri: HttpUrl = Field(default="https://oauth2.googleapis.com/token")
    auth_provider_x509_cert_url: HttpUrl = Field(default="https://www.googleapis.com/oauth2/v1/certs")
    client_secret: str
    redirect_uris: List[AnyHttpUrl] = Field(default=['http://localhost'])


class GoogleConfiguration(BaseModel):
    installed: Installed
