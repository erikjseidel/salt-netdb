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


def _call_cfdns_util(function, data=None, method='GET'):
    endpoint = _CFDNS_UTIL_NAME + '/' + function

    return __utils__['netdb_runner.call_netdb_util'](endpoint, data=data, method=method)


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

        salt-run ipam.update_cfdns test=False

    """

    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    if test:
        method = 'GET'
    else:
        method = 'POST'

    return _call_cfdns_util('update_cf', method=method)


def get_cfdns():
    """
    Return CF managed zones and PTR records.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if fetch successful; false otherwise
       * out: a dict of CF managed zones and PTR records and relevent attributes.

    CLI Example::

    .. code-block:: bash

        salt-run ipam.get_cfdns

    """
    method = 'GET'

    return _call_cfdns_util('get_cf', method=method)


def set_cfdns_zone(prefix, account, zone, managed, test=True):
    """
    Request addition / update of a CF managed zone identified by CIDR

    :param prefix:  Reverse DNS zone identified by CIDR
    :param account: Cloudflare account ID
    :param zone:    Cloudflare zone ID
    :param managed: If true any records in zone not matched by netdb will be deleted.
    :param test:    Perform the update if false, only list update actions if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if update / list IPs successful; false otherwise
       * out: a list of netdb managed PTRs in CF zones, relevent attributes and
              action required.

    CLI Example::

    .. code-block:: bash

        salt-run ipam.set_cfdns_zone 23.181.64.0/24 847e539c1cd80 224c1ba9e358 managed=True

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    if not isinstance(managed, bool):
        return {"result": False, "comment": "managed accepts true or false."}

    if test:
        method = 'GET'
    else:
        method = 'POST'

    data =  {
            "prefix"   :   prefix,
            "zone"     :   zone,
            "account"  :   account,
            "managed"  :   managed,
            }

    return _call_cfdns_util('set_cfzone', data=data, method=method)


def delete_cfdns_zone(prefix):
    """
    Request deletion of a CF managed zone identified by CIDR

    :param prefix:  Reverse DNS zone identified by CIDR
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if delete action successful; false otherwise

    CLI Example::

    .. code-block:: bash

        salt-run ipam.delete_cfdns_zone 23.181.64.0/24

    """
    method = 'DELETE'

    data =  {
            "prefix"   :   prefix,
            }

    return _call_cfdns_util('delete_cfzone', data=data, method=method)


def set_cfdns_token(token):
    """
    Request addition / update of CF bearer token used to access CF managed
    zones.

    :param token:  Cloudflare bearer token for managed zones
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise

    CLI Example::

    .. code-block:: bash

        salt-run ipam.set_cfdns_token MY_SECRET_TOKEN

    """
    method = 'POST'

    data =  {
            "token"   :   token,
            }

    return _call_cfdns_util('set_cftoken', data=data, method=method)
