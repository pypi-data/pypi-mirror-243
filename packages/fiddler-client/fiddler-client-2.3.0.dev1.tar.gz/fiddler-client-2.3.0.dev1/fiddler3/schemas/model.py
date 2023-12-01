from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic.fields import Field

from fiddler3.schemas.base import BaseModel
from fiddler3.schemas.model_schema import Column, ModelSchema
from fiddler3.schemas.model_spec import ModelSpec
from fiddler3.schemas.model_task_params import ModelTaskParams
from fiddler3.schemas.organization import OrganizationCompact
from fiddler3.schemas.project import ProjectCompact
from fiddler3.schemas.user import UserCompact
from fiddler3.schemas.xai_params import XaiParams


class ModelCompact(BaseModel):
    id: UUID
    name: str


class ModelResponse(BaseModel):
    id: UUID
    name: str
    input_type: str
    task: str
    task_params: ModelTaskParams
    schema_: ModelSchema = Field(alias='schema')
    spec: ModelSpec
    description: Optional[str]
    event_id_col: Optional[str]
    event_ts_col: Optional[str]
    event_ts_format: Optional[str]
    xai_params: Optional[XaiParams]
    artifact_status: str
    artifact_files: List[Dict]
    created_at: datetime
    updated_at: datetime
    created_by: UserCompact
    updated_by: UserCompact
    organization: OrganizationCompact
    project: ProjectCompact
    input_cols: List[Column]
    output_cols: List[Column]
    target_cols: List[Column]
    metadata_cols: List[Column]
    decision_cols: List[Column]
    is_binary_ranking_model: bool
