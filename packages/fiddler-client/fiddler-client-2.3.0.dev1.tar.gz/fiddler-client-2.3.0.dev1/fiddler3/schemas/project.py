from datetime import datetime
from uuid import UUID

from fiddler3.schemas.base import BaseModel
from fiddler3.schemas.organization import OrganizationCompact


class ProjectCompact(BaseModel):
    id: UUID
    name: str


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    organization: OrganizationCompact
