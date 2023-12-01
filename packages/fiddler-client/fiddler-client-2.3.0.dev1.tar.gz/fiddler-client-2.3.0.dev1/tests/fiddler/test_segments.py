from responses import matchers
from fiddler.schema.segment import Segment
from fiddler.exceptions import BadRequest
from tests.fiddler.base import BaseTestCase
from http import HTTPStatus


class TestSegment(BaseTestCase):

    def _get_url(self, uuid: str = None) -> str:
        base_url = f'{self._url}/segments'
        if uuid:
            return f'{base_url}/{uuid}'
        return base_url

    def test_get_segments(self):
        response = {
            "data": {
                "page_size": 50,
                "total": 2,
                "item_count": 2,
                "page_count": 1,
                "page_index": 1,
                "offset": 0,
                "items": [
                    {
                        "project_name": "bank_churn",
                        "name": "tp_0.8",
                        "model_name": "churn_classifier",
                        "definition": "age > 10",
                        "id": "fbba0596-1d49-4159-a5ea-e1c2f57c9c32",
                        "organization_name": "test_organization",
                        "description": "test description",
                        "extra_field_from_future": "should_not_break",
                        "created_at": "2021-03-03T18:30:00.000Z",
                        "created_by": {
                            "id": "1",
                            "full_name": "test user",
                            "email": "testuser@fiddler.ai"
                        }
                    },
                    {
                        "project_name": "bank_churn",
                        "name": "tp_0.6",
                        "model_name": "churn_classifier",
                        "definition": "credit_score > 600",
                        "id": "3a352397-a89a-495d-a095-440f1d21a58a",
                        "organization_name": "test_organization",
                        "description": "test description",
                        "created_at": "2021-03-03T18:30:00.000Z",
                        "created_by": {
                            "id": "2",
                            "full_name": "test user",
                            "email": "testuser@fiddler.ai"
                        }
                    }
                ]
            },
            "api_version": "2.0",
            "kind": "PAGINATED"
        }
        url = self._get_url()
        query_params = {
            'limit': 300,
            'offset': 0,
            'organization_name': 'test_organization',
            'project_name': 'bank_churn',
            'model_name': 'churn_classifier',
        }

        self.requests_mock.get(
            url, json=response, match=[matchers.query_param_matcher(query_params)]
        )

        segments = self.client.get_segments(
            project_id='bank_churn',
            model_id='churn_classifier',
        )
        assert segments == [
            Segment(
                id='fbba0596-1d49-4159-a5ea-e1c2f57c9c32',
                name='tp_0.8',
                definition='age > 10',
                organization_name='test_organization',
                project_name='bank_churn',
                model_name='churn_classifier',
                description='test description',
                created_at='2021-03-03T18:30:00.000Z',
                created_by={
                    "id": "1",
                    "full_name": "test user",
                    "email": "testuser@fiddler.ai"
                }
            ),
            Segment(
                id='3a352397-a89a-495d-a095-440f1d21a58a',
                name='tp_0.6',
                definition='credit_score > 600',
                organization_name='test_organization',
                project_name='bank_churn',
                model_name='churn_classifier',
                description='test description',
                created_at='2021-03-03T18:30:00.000Z',
                created_by={
                    "id": "2",
                    "full_name": "test user",
                    "email": "testuser@fiddler.ai"
                }
            ),
        ]

    def test_add_segment(self):
        response_body = {
            'data': {
                'id': 'fbba0596-1d49-4159-a5ea-e1c2f57c9c32',
            },
            'api_version': '2.0',
            'kind': 'NORMAL',
        }

        url = self._get_url()

        self.requests_mock.post(url, json=response_body)

        segment = self.client.add_segment(
            name='my segment',
            definition='age > 10',
            project_id='bank_churn',
            model_id='churn_classifier',
            description='test description',
        )
        assert segment == Segment(
            id='fbba0596-1d49-4159-a5ea-e1c2f57c9c32',
            name='my segment',
            definition='age > 10',
            organization_name='test_organization',
            project_name='bank_churn',
            model_name='churn_classifier',
            description='test description',
        )

    def test_add_segment_error(self):
        response_body = {
            'error': {
                'code': 400,
                'message': 'Column unknown not found in model churn_classifier',
                'errors': [
                    {
                        'reason': 'CustomMetricInvalidColumn',
                        'message': 'Column unknown not found in model churn_classifier',
                        'help': ''}
                ]
            },
            'api_version': '2.0',
            'kind': 'ERROR'
        }

        url = self._get_url()

        self.requests_mock.post(url, json=response_body, status=HTTPStatus.BAD_REQUEST)

        with self.assertRaises(BadRequest) as context:
            self.client.add_segment(
                name='my segment',
                definition='unknown > 10',
                project_id='bank_churn',
                model_id='churn_classifier',
            )
        self.assertEqual(
            context.exception.message,
            "Column unknown not found in model churn_classifier"
        )

    def test_get_segment(self):
        uuid = 'fbba0596-1d49-4159-a5ea-e1c2f57c9c32'
        response = {
            "data": {
                "project_name": "bank_churn",
                "name": "tp_0.8",
                "model_name": "churn_classifier",
                "definition": "age > 10",
                "id": "fbba0596-1d49-4159-a5ea-e1c2f57c9c32",
                "organization_name": "test_organization",
                "description": "test description",
                "extra_field_from_future": "should_not_break",
                "created_at": "2021-03-03T18:30:00.000Z",
                "created_by": {
                    "id": "1",
                    "full_name": "test user",
                    "email": "testuser@fiddler.ai"
                }
            },
            "api_version": "2.0",
            "kind": "NORMAL"
        }
        url = self._get_url(uuid)

        self.requests_mock.get(url, json=response)
        cm = self.client.get_segment(
            segment_id='fbba0596-1d49-4159-a5ea-e1c2f57c9c32'
        )
        assert cm == Segment(
            id='fbba0596-1d49-4159-a5ea-e1c2f57c9c32',
            name='tp_0.8',
            definition='age > 10',
            organization_name='test_organization',
            project_name='bank_churn',
            model_name='churn_classifier',
            description='test description',
            created_at='2021-03-03T18:30:00.000Z',
            created_by={
                "id": "1",
                "full_name": "test user",
                "email": "testuser@fiddler.ai"
            }
        )

    def test_delete_segment(self):
        uuid = 'fbba0596-1d49-4159-a5ea-e1c2f57c9c32'
        url = self._get_url(uuid)

        self.requests_mock.delete(url)

        self.client.delete_segment(
            segment_id='fbba0596-1d49-4159-a5ea-e1c2f57c9c32'
        )
        self.assertEqual(len(self.requests_mock.calls), 1)
