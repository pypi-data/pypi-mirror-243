from uuid import UUID

from pydantic import BaseModel


class UserCompact(BaseModel):
    id: UUID
    full_name: str
    email: str
