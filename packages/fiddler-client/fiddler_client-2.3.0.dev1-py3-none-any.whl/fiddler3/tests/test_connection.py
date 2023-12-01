from http import HTTPStatus

import pytest
import responses
from responses import matchers

from fiddler3.connection import Connection
from fiddler3.constants.common import CLIENT_NAME
from fiddler3.exceptions import ApiError
from fiddler3.tests.constants import URL
from fiddler3.version import __version__


@responses.activate
def test_version_compatibility_success(connection: Connection) -> None:
    params = {'client_name': CLIENT_NAME, 'client_version': __version__}
    responses.get(
        url=f'{URL}/v3/version-compatibility',
        json={},
        match=[matchers.query_param_matcher(params)],
    )

    connection._check_version_compatibility()


@responses.activate
def test_version_compatibility_failed(connection: Connection) -> None:
    responses.get(
        url=f'{URL}/v3/version-compatibility',
        json={
            'error': {
                'code': HTTPStatus.BAD_REQUEST,
                'message': 'You are using old fiddler-client version. Please upgrade to 3.x or above',
                'errors': [],
            }
        },
        status=HTTPStatus.BAD_REQUEST,
    )

    with pytest.raises(ApiError):
        connection._check_version_compatibility()
