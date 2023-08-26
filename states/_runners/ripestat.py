import logging, copy
from netaddr   import IPSet
from ipaddress import ip_interface, ip_network
from copy      import deepcopy

__virtualname__ = "ripestat"

_PM_UTIL_NAME = 'ripe'

log = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__


def _call_ripe_util(function, data=None, params=None, method='GET', test=True):
    endpoint = _PM_UTIL_NAME + '/' + function

    return __utils__['netdb_util.call_netdb_util'](endpoint, data=data, params=params, method=method, test=test)


def get_paths(prefix):
    """
    Set a Peering Manager session to maintenance and synchronize netdb.

    :param device: the device where session is located.
    :param neighbor: the neighbor IP address of the session.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.set_maintenance sin2 169.254.169.254

    """
    params = {
            'prefix' : prefix,
            }

    return _call_ripe_util('get_paths', params=params)
