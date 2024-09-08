import logging

from netdb_util_api import NetdbUtilAPI

__virtualname__ = "ripestat"

_ENDPOINT = 'utility/ripe/{}'

log = logging.getLogger(__file__)


def __virtual__():
    return __virtualname__


def get_paths(prefix: str) -> dict:
    """
    Get matching AS paths frpm RipeStat API.

    :param prefix: The prefix to check
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of RipeStat results

    CLI Example::

    .. code-block:: bash

        salt-run ripestat.get_paths 23.181.64.0/24

    """
    params = {'prefix': prefix}

    return NetdbUtilAPI(__salt__['pillar.show_pillar']()).get(
        _ENDPOINT.format('paths'), params=params
    )
