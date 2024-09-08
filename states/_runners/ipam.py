import logging

__virtualname__ = 'ipam'

_IPAM_UTIL_EP = 'utility/ipam'

logger = logging.getLogger(__file__)

_WARNING = """This utility returns only ip space that is managed by salt-netdb. In order for
it to return accurate free space, the entirety of the queried prefix must be
managed by salt-netdb. 
"""


def __virtual__():
    return __virtualname__


def _call_ipam_util(function, params=None):
    endpoint = f'{_IPAM_UTIL_EP}/{function}'

    return __utils__['netdb_util.call_netdb_util'](endpoint, params=params)


def report():
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
    return _call_ipam_util('report')


def chooser(prefix):
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

    ret = _call_ipam_util('chooser', params=params)

    ret.update({'notice': _WARNING})

    return ret
