import logging
from netdb_util_api import NetdbUtilAPI

__virtualname__ = "ipam"

_ENDPOINT = 'utility/ipam/{}'

logger = logging.getLogger(__file__)

_WARNING = """This utility returns only ip space that is managed by salt-netdb. In order for
it to return accurate free space, the entirety of the queried prefix must be
managed by salt-netdb. 
"""


def __virtual__():
    return __virtualname__


def report() -> dict:
    """
    Show salt managed IP addresses.

    A sorted list of salt managed IP addresses is also displayed in the
    comment.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if IP addresses returned; false otherwise

    CLI Example::

    .. code-block:: bash

        salt-run ipam.report

    """
    return NetdbUtilAPI(__salt__['pillar.show_pillar']()).get(
        _ENDPOINT.format('report')
    )


def chooser(prefix: str) -> dict:
    """
    Show available prefixes / free IP space within a given (super)prefix.

    In order for this function to by accurate, all IP a space within the
    the queried prefix must be managed by netdb - salt.

    :param prefix: The prefix whose free space is to be returned.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if IP addresses returned; false otherwise
       * out: a list of free space in prefix and range formats

    CLI Example::

    .. code-block:: bash

        salt-run ipam.chooser prefix='23.181.64.0/24'

    """
    params = {"prefix": prefix}

    ret = NetdbUtilAPI(__salt__['pillar.show_pillar']()).get(
        _ENDPOINT.format('chooser'), params=params
    )

    ret.update({'notice': _WARNING})

    return ret
