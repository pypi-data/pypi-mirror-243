from datetime import datetime
from typing import Optional

from fiddler.schema.base import BaseDataSchema
from fiddler.schema.user import UserCompact


class Segment(BaseDataSchema):
    id: str
    name: str
    project_name: str
    organization_name: str
    definition: str
    description: Optional[str]
    created_at: Optional[datetime]
    created_by: Optional[UserCompact]
