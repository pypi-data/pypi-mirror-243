from uuid import UUID

from fiddler3.schemas.base import BaseModel


class OrganizationCompact(BaseModel):
    id: UUID
    name: str
