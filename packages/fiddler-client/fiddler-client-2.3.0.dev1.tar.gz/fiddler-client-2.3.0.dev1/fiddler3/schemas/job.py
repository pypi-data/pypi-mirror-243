from typing import Optional
from uuid import UUID

from fiddler3.schemas.base import BaseModel


class JobCompact(BaseModel):
    id: UUID
    name: str


class JobResponse(BaseModel):
    id: UUID
    name: str
    status: str
    progress: float
    error_message: Optional[str]
    error_reason: Optional[str]
    extras: Optional[dict]
