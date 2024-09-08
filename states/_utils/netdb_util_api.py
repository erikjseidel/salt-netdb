from typing import Optional
import requests

from salt.exceptions import SaltException

NETDB_UTIL_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

__virtual_name__ = "netdb_util_api"


NETDB_PILLAR = 'netdb'


def __virtual__():
    return __virtual_name__


class NetdbUtilAPI:

    # NetDB Util service URL base
    util_url: str

    def __init__(self, pillar):
        """
        NetdbUtilAPI is used to interact with the NetDB util service.

        pillar: dict
            A dict containing a 'netdb' key with netdb pillar data and
            an optional 'netdb_local' key containing the netdb_local
            pillar data.
        """

        self.util_url = pillar[NETDB_PILLAR]['util_url']

    def _request(
        self,
        endpoint: str,
        method: str,
        data: Optional[dict],
        params: Optional[dict],
        test: bool,
    ) -> dict:
        """
        Internal request handler for sending requests to the NetDB util service

        """
        params = params or {}

        url = self.util_url + endpoint

        resp = requests.request(
            url=url,
            method=method,
            headers=NETDB_UTIL_HEADERS,
            params=params,
            json=data,
            verify=False,
            cert=None,
        )

        if (code := resp.status_code) not in [200, 400, 404, 422]:
            raise SaltException(f'NetDB Util API error: {url}: {code}: {resp.reason}')

        if not (ret_dict := resp.json()):
            raise SaltException(
                f'NetDB Util returned unexpected empty JSON response. Status code {code}'
            )

        return ret_dict

    def get(
        self, endpoint: str, params: Optional[dict] = None, test: bool = True
    ) -> dict:
        """
        Send a GET request to the NetDB Util service

        endpoint: str
            NetDB util endpoint to query

        params: dict
            HTTP query parameters

        test: bool
            If true tell NetDB util to do a dry run and not commit any changes

        """
        return self._request(endpoint, 'GET', None, params, test)

    def post(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        test: bool = True,
    ) -> dict:
        """
        Send a POST request to the NetDB Util service

        endpoint: str
            NetDB util endpoint to query

        data: dict
            JSON HTTP body data to send to the API

        params: dict
            HTTP query parameters

        test: bool
            If true tell NetDB util to do a dry run and not commit any changes

        """
        return self._request(endpoint, 'POST', data, params, test)

    def put(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        test: bool = True,
    ) -> dict:
        """
        Send a PUT request to the NetDB Util service

        endpoint: str
            NetDB util endpoint to query

        data: dict
            JSON HTTP body data to send to the API

        params: dict
            HTTP query parameters

        test: bool
            If true tell NetDB util to do a dry run and not commit any changes

        """
        return self._request(endpoint, 'PUT', data, params, test)

    def delete(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        test: bool = True,
    ) -> dict:
        """
        Send a DELETE request to the NetDB Util service

        endpoint: str
            NetDB util endpoint to query

        data: dict
            JSON HTTP body data to send to the API

        params: dict
            HTTP query parameters

        test: bool
            If true tell NetDB util to do a dry run and not commit any changes

        """
        return self._request(endpoint, 'DELETE', data, params, test)
