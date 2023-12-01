from __future__ import annotations

from typing import Iterator, TypeVar

from requests import Response

from fiddler3 import Connection
from fiddler3.configs import DEFAULT_PAGE_SIZE
from fiddler3.libs.http_client import RequestClient
from fiddler3.schemas.response import PaginatedApiResponse

BaseEntityType = TypeVar(  # pylint: disable=invalid-name
    'BaseEntityType', bound='BaseEntity'
)


class BaseEntity:
    @classmethod
    def _connection(cls) -> Connection:
        """Fiddler connection instance"""
        from fiddler3 import connection

        assert connection is not None
        return connection

    @classmethod
    def _client(cls) -> RequestClient:
        """Request client instance"""
        return cls._connection().client

    @classmethod
    def _from_response(cls: type[BaseEntityType], response: Response) -> BaseEntityType:
        """Build entity object from the given response"""
        return cls._from_dict(data=response.json()['data'])

    @classmethod
    def _from_dict(cls: type[BaseEntityType], data: dict) -> BaseEntityType:
        """Build entity object from the given dictionary"""
        raise NotImplementedError()

    @classmethod
    def _paginate(
        cls, url: str, params: dict | None = None, page_size: int = DEFAULT_PAGE_SIZE
    ) -> Iterator[dict]:
        """
        Iterator over pagination API
        :param url: Pagination endpoint
        :param page_size: Number of items per page
        :return: Iterator of items
        """
        offset = 0
        params = params or {}
        params.update(
            {
                'limit': page_size,
                'offset': offset,
            }
        )

        while True:
            response = cls._client().get(
                url=url,
                params={
                    'limit': page_size,
                    'offset': offset,
                },
            )
            resp_obj = PaginatedApiResponse(**response.json()).data

            if resp_obj.page_count == resp_obj.page_index:
                break

            yield from resp_obj.items

            # Update offset
            offset = resp_obj.offset + page_size
