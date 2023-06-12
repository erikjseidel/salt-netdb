import logging, copy
from netaddr   import IPSet
from ipaddress import ip_interface, ip_network
from copy      import deepcopy

__virtualname__ = "pm"

_PM_UTIL_NAME = 'pm'

log = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__


def _call_pm_util(function, data=None, params=None, test=True):
    endpoint = _PM_UTIL_NAME + '/' + function

    return __utils__['netdb_runner.call_netdb_util'](endpoint, data=data, params=params, test=test)


def generate_direct_sessions():
    """
    Show eBGP direct session config generated from Peering Manager source 
    in netdb format.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of devices in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run pm.generate_direct_sessions

    """
    return _call_pm_util('generate_direct_sessions')


def generate_ixp_sessions():
    """
    Show eBGP IXP session config generated from Peering Manager source 
    in netdb format.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of devices in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run pm.generate_ixp_sessions

    """
    return _call_pm_util('generate_ixp_sessions')


def synchronize_sessions(test=True):
    """
    Load eBGP config generated from Peering Manager source into netdb.

    :param test: Synchonize all devices if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.synchronize_sessions
        salt-run pm.synchronize_sessions test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_pm_util('synchronize_sessions', test=test)
