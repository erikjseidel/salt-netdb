# -*- coding: utf-8 -*-

import logging, copy
from netaddr   import IPSet
from ipaddress import ip_interface, ip_network
from copy      import deepcopy

__virtualname__ = "ipam"

_IPAM_UTIL_NAME  = 'ipam'
_CFDNS_UTIL_NAME = 'cfdns'

log = logging.getLogger(__file__)

_WARNING = """This utility returns only ip space that is managed by salt-netdb. In order for
it to return accurate free space, the entirety of the queried prefix must be
managed by salt-netdb. 
"""

def __virtual__():
    return __virtualname__


def _call_ipam_util(function, data, out=True, comment=True):
    endpoint = _IPAM_UTIL_NAME + '/' + function

    ret = __utils__['netdb_runner.call_netdb_util'](endpoint, data = data)

    if not out:
        ret.pop('out', None)
    if not comment:
        ret.pop('comment', None)

    return ret


def _call_cfdns_util(function, method='GET'):
    endpoint = _CFDNS_UTIL_NAME + '/' + function

    return __utils__['netdb_runner.call_netdb_util'](endpoint, method=method)


def report(device = None, out = True, comment = True):
    """
    Show salt managed IP addresses.

    A sorted list of salt managed IP addresses is also displayed in the
    comment.

    :param device: Limit report to only the specified device.
    :param out: Suppresses serialized dictionary out put if False.
    :param comment: Suppresses sorted list output to comment put if False.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if IP addresses returned; false otherwise

    CLI Example::

    .. code-block:: bash

        salt-run ipam.report
        salt-run ipam.report sin1 comment=False

    """

    if not isinstance(out, bool) or not isinstance(comment, bool):
        return {"result": False, "comment": "comment and out only accept true or false."}

    if device:
        filt = { "device": device }
    else:
        filt = None

    return _call_ipam_util('report', filt, out, comment)


def chooser(prefix, out=True, comment=True):
    """
    Show available prefixes / free IP space within a given (super)prefix.

    In order for this function to by accurate, all IP a space within the
    the queried prefix must be managed by netdb - salt.

    :param prefix: The prefix whose free space is to be returned.
    :param out: Suppresses serialized dictionary out put if False.
    :param comment: Suppresses sorted list output to comment put if False.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if IP addresses returned; false otherwise
       * out: a list of free space in prefix and range formats

    CLI Example::

    .. code-block:: bash

        salt-run ipam.chooser prefix='23.181.64.0/24'

    """
    if not isinstance(out, bool) or not isinstance(comment, bool):
        return {"result": False, "comment": "comment and out only accept true or false."}

    data = { "prefix": prefix }

    ret = _call_ipam_util('chooser', data, out, comment)

    ret.update({'notice': _WARNING})

    return ret


def update_cfdns(test=True):
    """
    Request update for netdb-util managed Cloudflare PTR zones.

    :param test: Perform the update if false, only list update actions if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if update / list IPs successful; false otherwise
       * out: a list of netdb managed PTRs in CF zones, relevent attributes and
              action required.

    ptr['action'] values are:
       * create: PTR does not exist in CF zone. Record will be created
       * update: PTR exists but does not match netdb record; will be updated
       * delete: PTR in CF zone does not exist in netdb; will be deleted
       * pass:   CF and netdb records align. No action required.

    CLI Example::

    .. code-block:: bash

        salt-run ipam.chooser prefix='23.181.64.0/24'

    """

    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    if test:
        method = 'GET'
    else:
        method = 'POST'

    return _call_cfdns_util('update_cf', method=method)
