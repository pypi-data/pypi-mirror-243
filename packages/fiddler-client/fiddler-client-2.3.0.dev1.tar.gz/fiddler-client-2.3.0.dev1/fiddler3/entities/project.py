from __future__ import annotations

from datetime import datetime
from typing import Iterator
from uuid import UUID

from fiddler3.decorators import handle_api_error
from fiddler3.entities.base import BaseEntity
from fiddler3.entities.helpers import raise_not_found
from fiddler3.schemas.project import ProjectResponse


class Project(BaseEntity):
    def __init__(self, name: str) -> None:
        """
        Construct a project instance
        :param name: Slug like name
        """
        self.name = name

        self.id: UUID | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

        # Deserialized response object
        self._resp: ProjectResponse | None = None

    @staticmethod
    def _get_url(id_: UUID | str | None = None) -> str:
        """Get project resource/item url"""
        url = '/v3/projects'
        return url if not id_ else f'{url}/{id_}'

    @classmethod
    def _from_dict(cls, data: dict) -> Project:
        """Build entity object from the given dictionary"""

        # Deserialize the response
        resp_obj = ProjectResponse(**data)

        # Initialize
        instance = cls(
            name=resp_obj.name,
        )

        # Add remaining fields
        fields = ['id', 'created_at', 'updated_at']
        for field in fields:
            setattr(instance, field, getattr(resp_obj, field, None))

        instance._resp = resp_obj
        return instance

    @classmethod
    @handle_api_error
    def get(cls, id_: UUID | str) -> Project:
        """Get the project instance using project id"""
        response = cls._client().get(url=cls._get_url(id_))
        return cls._from_response(response=response)

    @classmethod
    @handle_api_error
    def from_name(cls, name: str) -> Project:
        """Get the project instance using project name"""
        response = cls._client().get(url=cls._get_url(), params={'name': name})
        if response.json()['data']['total'] == 0:
            raise_not_found('Project not found for the given identifier')

        return cls._from_dict(data=response.json()['data']['items'][0])

    @classmethod
    @handle_api_error
    def list(cls) -> Iterator[Project]:
        """
        Get a list of all projects in the organization
        """
        for project in cls._paginate(url=cls._get_url()):
            yield cls._from_dict(data=project)

    @handle_api_error
    def create(self) -> Project:
        """Create a new project"""
        response = self._client().post(url=self._get_url(), data={'name': self.name})
        return self._from_response(response=response)

    @handle_api_error
    def delete(self) -> None:
        """Delete project"""
        # @TODO - Switch this to v3 once we have the endpoint
        self._client().delete(url=f'/v2/projects/{self.id}')
