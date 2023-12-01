from http import HTTPStatus
from typing import List, Optional

from pydantic import parse_obj_as

from fiddler.libs.http_client import RequestClient
from fiddler.schema.segment import Segment
from fiddler.utils.decorators import handle_api_error_response
from fiddler.utils.logger import get_logger
from fiddler.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = get_logger(__name__)


class SegmentsMixin:

    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def add_segment(
        self,
        name: str,
        project_id: str,
        model_id: str,
        definition: str,
        description: Optional[str] = None,
    ) -> Segment:
        """
        Add a new `Segment`.

        :params name: name of segment
        :params project_id: name of project
        :params model_id: name of model
        :params definition: The FQL expression describing the segment
        :params description: description of segment

        :returns: Created `Segment` object.
        """
        attrs = {
            'organization_name': self.organization_name,
            'project_name': project_id,
            'model_name': model_id,
            'name': name,
            'definition': definition,
            'description': description,
        }
        response = self.client.post(
            url='segments',
            data=attrs,
        )
        response_data = APIResponseHandler(response)
        segment_id = response_data.get_data().get('id')
        attrs['id'] = segment_id
        return Segment.parse_obj(attrs)

    @handle_api_error_response
    def delete_segment(self, segment_id: str) -> None:
        """
        Delete a segment

        :params uuid: id of the segment to delete
        :returns: None
        """
        response = self.client.delete(
            url=f'segments/{segment_id}'
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'Segment {segment_id} deleted successfully.')
        else:
            logger.info('Segment deletion unsuccessful')

    @handle_api_error_response
    def get_segments(
        self,
        project_id: str,
        model_id: str,
        limit: int = 300,
        offset: int = 0
    ) -> List[Segment]:
        """
        Get a list of `Segment` objects.

        :params project_id: name of project
        :params model_id: name of model
        :params limit: number of segments to return
        :params offset: offset to start from

        :returns: a list of `Segment` objects
        """
        params = {
            'organization_name': self.organization_name,
            'project_name': project_id,
            'model_name': model_id,
            'offset': offset,
            'limit': limit,
        }
        response = self.client.get(
            url=f'segments',
            params=params
        )
        items = PaginatedResponseHandler(response).get_pagination_items()
        return parse_obj_as(List[Segment], items)

    @handle_api_error_response
    def get_segment(self, segment_id: str) -> Segment:
        """
        Get a `Segment` object.

        :params segment_id: id of the segment

        :returns: a `Segment` object
        """
        response = self.client.get(url=f'segments/{segment_id}')
        return Segment.deserialize(APIResponseHandler(response))
