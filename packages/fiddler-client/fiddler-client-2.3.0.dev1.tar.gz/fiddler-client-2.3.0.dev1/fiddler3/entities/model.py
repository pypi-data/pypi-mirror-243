from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

import pandas as pd

from fiddler3.constants.model import ModelInputType, ModelTask
from fiddler3.decorators import handle_api_error
from fiddler3.entities.base import BaseEntity
from fiddler3.entities.helpers import raise_not_found
from fiddler3.entities.job import Job
from fiddler3.schemas.job import JobCompact
from fiddler3.schemas.model import ModelResponse
from fiddler3.schemas.model_schema import Column, ModelSchema
from fiddler3.schemas.model_spec import ModelSpec
from fiddler3.schemas.model_task_params import ModelTaskParams
from fiddler3.schemas.xai_params import XaiParams
from fiddler3.utils.logger import get_logger
from fiddler3.utils.model_schema_generator import SchemaGeneratorFactory

logger = get_logger(__name__)


class Model(BaseEntity):
    def __init__(
        self,
        name: str,
        project_id: UUID,
        schema: ModelSchema,
        spec: ModelSpec | None = None,
        input_type: str = ModelInputType.TABULAR,
        task: str = ModelTask.NOT_SET,
        task_params: ModelTaskParams | None = None,
        description: str | None = None,
        event_id_col: str | None = None,
        event_ts_col: str | None = None,
        event_ts_format: str | None = None,
        xai_params: XaiParams | None = None,
    ) -> None:
        """
        Construct a model instance
        """
        self.name = name
        self.project_id = project_id
        self.schema = schema
        self.input_type = input_type
        self.task = task
        self.description = description
        self.event_id_col = event_id_col
        self.event_ts_col = event_ts_col
        self.event_ts_format = event_ts_format
        self.spec = spec or ModelSpec()
        self.task_params = task_params or ModelTaskParams()
        self.xai_params = xai_params or XaiParams()

        self.id: UUID | None = None
        self.artifact_status: str | None = None
        self.artifact_files: list[dict] | None = None
        self.input_cols: list[Column] | None = None
        self.output_cols: list[Column] | None = None
        self.target_cols: list[Column] | None = None
        self.metadata_cols: list[Column] | None = None
        self.decision_cols: list[Column] | None = None
        self.is_binary_ranking_model: bool | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

        # Deserialized response object
        self._resp: ModelResponse | None = None

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get model resource/item url"""
        url = '/v3/models'
        return url if not id_ else f'{url}/{id_}'

    @classmethod
    def _from_dict(cls, data: dict) -> Model:
        """Build entity object from the given dictionary"""

        # Deserialize the response
        resp_obj = ModelResponse(**data)

        # Initialize
        instance = cls(
            name=resp_obj.name,
            schema=resp_obj.schema_,
            spec=resp_obj.spec,
            project_id=resp_obj.project.id,
            input_type=resp_obj.input_type,
            task=resp_obj.task,
            task_params=resp_obj.task_params,
            description=resp_obj.description,
            event_id_col=resp_obj.event_id_col,
            event_ts_col=resp_obj.event_ts_col,
            event_ts_format=resp_obj.event_ts_format,
            xai_params=resp_obj.xai_params,
        )

        # Add remaining fields
        fields = [
            'id',
            'created_at',
            'updated_at',
            'artifact_status',
            'artifact_files',
            'input_cols',
            'output_cols',
            'target_cols',
            'metadata_cols',
            'decision_cols',
            'is_binary_ranking_model',
        ]
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj
        return instance

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str) -> Model:
        """Get the model instance using model id"""
        response = cls._client().get(url=cls._get_url(id_))
        return cls._from_response(response=response)

    @classmethod
    @handle_api_error
    def from_name(cls, model_name: str, project_name: str) -> Model:
        """Get the model instance using model name and project name"""
        response = cls._client().get(
            url=cls._get_url(),
            params={'name': model_name, 'project_name': project_name},
        )
        if response.json()['data']['total'] == 0:
            raise_not_found('Model not found for the given identifier')

        return cls._from_dict(data=response.json()['data']['items'][0])

    @handle_api_error
    def create(self) -> Model:
        """Create a new model"""
        response = self._client().post(
            url=self._get_url(),
            data={
                'name': self.name,
                'project_id': str(self.project_id),
                'schema': self.schema.dict(),
                'spec': self.spec.dict(),
                'input_type': self.input_type,
                'task': self.task,
                'task_params': self.task_params.dict(),
                'description': self.description,
                'event_id_col': self.event_id_col,
                'event_ts_col': self.event_ts_col,
                'event_ts_format': self.event_ts_format,
                'xai_params': self.xai_params.dict(),
            },
        )
        return self._from_response(response=response)

    @classmethod
    @handle_api_error
    def generate_schema(
        cls,
        source: pd.DataFrame | Path | list[dict[str, Any]] | str,
        max_cardinality: int | None = None,
        sample_size: int | None = None,
        enrich: bool = True,
    ) -> ModelSchema:
        """
        Generate model schema from the given data
        :param source: Data source - Dataframe or path to csv or parquet file.
        :param max_cardinality: Max cardinality to detect categorical columns
        :param sample_size: No. of samples to use for generating schema
        :param enrich: Enrich the model schema client side by scanning all data
        :return: Generated ModelSchema object
        """
        schema_generator = SchemaGeneratorFactory.create(
            source=source,
            max_cardinality=max_cardinality,
            sample_size=sample_size,
            enrich=enrich,
        )

        return schema_generator.generate(client=cls._client())

    @handle_api_error
    def delete(self) -> Job:
        """Delete a model and it's associated resources"""
        assert self.id is not None
        response = self._client().delete(url=self._get_url(id_=self.id))

        job_compact = JobCompact(**response.json()['data']['job'])
        return Job.get(id_=job_compact.id)
