import pytest
from pytest_mock import MockerFixture

from fiddler3 import Connection
from fiddler3.schemas.server_info import ServerInfo
from fiddler3.tests.constants import ORG_ID, ORG_NAME, SERVER_VERSION, TOKEN, URL


@pytest.fixture(autouse=True, scope='session')
def connection(session_mocker: MockerFixture) -> Connection:
    """Connection instance"""
    conn = Connection(
        url=URL,
        token=TOKEN,
        validate=False,
    )

    server_info = ServerInfo(
        **{
            'feature_flags': {},
            'server_version': SERVER_VERSION,
            'organization': {
                'id': ORG_ID,
                'name': ORG_NAME,
            },
        }
    )
    session_mocker.patch.object(conn, '_get_server_info', server_info)
    session_mocker.patch('fiddler3.connection', conn)
    yield conn
