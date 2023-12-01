from typing import Dict, Generator

from fiddler3.libs.semver import VersionInfo
from fiddler3.schemas.base import BaseModel
from fiddler3.schemas.organization import OrganizationCompact


class Version(VersionInfo):
    @classmethod
    def __get_validators__(cls) -> Generator:
        """Return a list of validator methods for pydantic models."""
        yield cls.parse


class ServerInfo(BaseModel):
    feature_flags: Dict
    server_version: Version
    organization: OrganizationCompact
