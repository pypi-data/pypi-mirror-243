from __future__ import annotations

from copy import deepcopy
from typing import Any
from urllib.parse import urljoin

import requests
import simplejson
from requests.adapters import HTTPAdapter
from requests_toolbelt.multipart.encoder import MultipartEncoder

from fiddler3.constants.common import JSON_CONTENT_TYPE
from fiddler3.exceptions import ConnectionError, ConnectionTimeout, HttpError
from fiddler3.utils.logger import get_logger

logger = get_logger(__name__)


class RequestClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str],
        verify: bool = True,
        proxies: dict | None = None,
    ) -> None:
        self.base_url = base_url
        self.proxies = proxies
        self.headers = headers
        self.headers.update({'Content-Type': JSON_CONTENT_TYPE})
        self.session = requests.Session()
        self.session.verify = verify
        adapter = HTTPAdapter(
            pool_connections=25,
            pool_maxsize=25,
        )
        self.session.mount(self.base_url, adapter)

    def call(
        self,
        *,
        method: str,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        data: dict | None = None,
        timeout: int | None = None,
        files_encoders: dict[str, MultipartEncoder] | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Make request to server

        :param method: HTTP method like
        :param url: API endpoint
        :param params: Query parameters
        :param headers: Request headers
        :param data: Dict/binary data
        :param timeout: Request timeout in seconds
        :param files_encoders:  Dictionary of 'filename': file-like-objects
            for multipart encoding upload. Make sure all MultipartEncoder values have
            same content_type.
        """
        logger.debug('Making %s call to %s', method, url)

        full_url = urljoin(self.base_url, url)

        request_headers = self.headers
        # override/update headers coming from the calling method
        if headers:
            request_headers = deepcopy(self.headers)
            request_headers.update(headers)

        content_type = request_headers.get('Content-Type')
        if data and content_type == JSON_CONTENT_TYPE:
            data = simplejson.dumps(data, ignore_nan=True)  # type: ignore

        kwargs.setdefault('allow_redirects', True)
        # requests is not able to pass the value of self.session.verify to the
        # verify param in kwargs when REQUESTS_CA_BUNDLE is set.
        # So setting that as default here
        kwargs.setdefault('verify', self.session.verify)
        try:
            if files_encoders:
                encoders = list(files_encoders.values())
                if encoders:
                    request_headers['Content-Type'] = encoders[0].content_type
                response = self.session.request(
                    method,
                    full_url,
                    params=params,
                    files=files_encoders,
                    headers=request_headers,
                    timeout=timeout,
                    proxies=self.proxies,
                    **kwargs,
                )
            else:
                response = self.session.request(
                    method,
                    full_url,
                    params=params,
                    data=data,
                    headers=request_headers,
                    timeout=timeout,
                    proxies=self.proxies,
                    **kwargs,
                )

        except requests.Timeout:
            logger.error(f'{method} call failed with Timeout error for URL {url}')
            raise ConnectionTimeout()
        except requests.ConnectionError:
            logger.error(f'{method} call failed with ConnectionError for URL {url}')
            raise ConnectionError()
        except requests.RequestException:
            # catastrophic error.
            logger.error(f'{method} call failed with RequestException for URL {url}')
            raise HttpError()

        response.raise_for_status()
        return response

    def get(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        return self.call(
            method='GET',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def delete(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        return self.call(
            method='DELETE',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def post(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | None = None,
        files_encoders: dict[str, MultipartEncoder] | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        return self.call(
            method='POST',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            files_encoders=files_encoders,
            **kwargs,
        )

    def put(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        return self.call(
            method='PUT',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )

    def patch(
        self,
        *,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
        timeout: int | None = None,
        data: dict | None = None,
        **kwargs: dict[str, Any],
    ) -> requests.Response:
        return self.call(
            method='PATCH',
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
            data=data,
            **kwargs,
        )
