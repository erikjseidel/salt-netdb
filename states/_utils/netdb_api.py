from typing import Optional
import logging
import requests

from exceptions.netdb_exceptions import ColumnNotFoundException

from salt.exceptions import SaltException

__virtual_name__ = 'netdb_api'

logger = logging.getLogger(__file__)

NETDB_PILLAR = 'netdb'
NETDB_LOCAL_PILLAR = 'netdb_local'

NETDB_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def __virtual__():
    return __virtual_name__


class NetdbAPI:

    # Base URL of netdb server
    netdb_url: str

    # Base URL of netdb local server
    netdb_local_url: Optional[str] = None

    def __init__(self, pillar: dict):
        """
        NetdbAPI instance is used to interact with the NetDB service.

        pillar: dict
            A dict containing a 'netdb' key with netdb pillar data and
            an optional 'netdb_local' key containing the netdb_local
            pillar data.

        """
        netdb = pillar[NETDB_PILLAR]
        netdb_local = pillar.get(NETDB_LOCAL_PILLAR)

        self.netdb_url = netdb['url']

        if netdb_local and netdb_local.get('enabled'):
            self.netdb_url = netdb_local['url']

    def get(self, endpoint: str) -> dict:
        """
        Make a get request against NetDB service.

        endpoint: str
            NetDB endpoint to query, e.g. '/column/bgp'

        """
        url = (self.netdb_local_url or self.netdb_url) + endpoint

        resp = requests.get(url=url, headers=NETDB_HEADERS, verify=False, cert=None)

        if (code := resp.status_code) not in [200, 404, 422]:
            raise SaltException(f'NetDB API error: {url}: {code}: {resp.reason}')

        if not (ret_dict := resp.json()):
            raise SaltException(
                f'NetDB returned unexpected empty JSON response. Status code {code}'
            )

        if not ret_dict.get('result'):
            raise ColumnNotFoundException(ret_dict['comment'])

        return ret_dict

    def list_columns(self) -> list:
        """
        Return a list of available columns.
        """
        return self.get('column')

    def get_column(self, router: str, column: str) -> Optional[dict]:
        """
        Retrieves a column from netdb for the device. Used by column module
        'get', 'items' and 'keys' functions.

        router: str
            Router ID (e.g. __grains__['id'])

        column: str
            Name of column to retrieve

        """
        return self.get(f'column/{column}/{router}')['out'][router]


def get_api(pillar: dict) -> NetdbAPI:
    """
    Wrapper function to instantiate a NetdbAPI class from the utils dunder dict.

    pillar: dict
        A dict containing a 'netdb' key with netdb pillar data and
        an optional 'netdb_local' key containing the netdb_local
        pillar data.

    """
    return NetdbAPI(pillar)
