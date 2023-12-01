from __future__ import annotations

from fiddler3.configs import DEFAULT_CONNECTION_TIMEOUT
from fiddler3.connection import Connection
from fiddler3.entities import *  # noqa
from fiddler3.exceptions import *  # noqa
from fiddler3.schemas import *  # noqa

# Global connection object
connection: Connection | None = None


def init(
    url: str,
    token: str,
    proxies: dict | None = None,
    timeout: int = DEFAULT_CONNECTION_TIMEOUT,
    verify: bool = True,
    validate: bool = True,
) -> None:
    """
    Initiate Python Client Connection
    :param url: URL of Fiddler Platform
    :param token: Authorization token
    :param proxies: Dictionary mapping protocol to the URL of the proxy
    :param timeout: Seconds to wait for the server to send data before giving up
    :param verify: Controls whether we verify the server’s TLS certificate
    :param validate: Whether to validate the server/client version compatibility.
         Some functionalities might not work if this is turned off.
    """
    global connection
    connection = Connection(
        url=url,
        token=token,
        proxies=proxies,
        timeout=timeout,
        verify=verify,
        validate=validate,
    )
