# -*- coding: utf-8 -*-

import logging, copy
from netaddr   import IPSet
from ipaddress import ip_interface, ip_network
from copy      import deepcopy

__virtualname__ = "netbox"

_NETBOX_UTIL_NAME = 'netbox'

log = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__


def _call_netbox_util(function, data=None, params=None, test=True):
    endpoint = _NETBOX_UTIL_NAME + '/' + function

    return __utils__['netdb_runner.call_netdb_util'](endpoint, data=data, params=params, test=test)


def generate_devices():
    """
    Show devices generated from Netbox source in netdb format.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of devices in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run netbox.generate_devices

    """
    return _call_netbox_util('generate_devices')


def generate_interfaces(device):
    """
    Show interfaces generated from Netbox source in netdb format for a device.

    :param device: The device whose interfaces are to be generated.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of interfaces in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run netbox.generate_interfaces sin1

    """
    data = { "device": device }

    ret = _call_netbox_util('generate_interfaces', data)

    return ret


def generate_isis():
    """
    Show IS-IS config generated from Netbox source in netdb format.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of devices in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run netbox.generate_isis

    """
    return _call_netbox_util('generate_igp')


def generate_ebgp():
    """
    Show internal eBGP config generated from Netbox source in netdb format.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of devices in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run netbox.generate_ebgp

    """
    return _call_netbox_util('generate_ebgp')


def synchronize_devices(test=True):
    """
    Load devices generated from Netbox source into netdb.

    :param test: Synchonize devices if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.synchronize_devices

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_netbox_util('synchronize_devices', test=test)


def synchronize_interfaces(devices, test=True):
    """
    Load interfaces generated from Netbox source into netdb for a device.

    :param devices: Comma separated list of devices be updated.
    :param test: Synchonize interfaces if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.synchronize_interfaces sin1

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    devs = devices.split(',')

    data = { "devices": devs }

    return _call_netbox_util('synchronize_interfaces', data, test=test)


def synchronize_isis(test=True):
    """
    Load IS-IS config generated from Netbox source into netdb.

    :param test: Synchonize all devices if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.synchronize_isis
        salt-run netbox.synchronize_isis test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_netbox_util('synchronize_igp', test=test)


def synchronize_ebgp(test=True):
    """
    Load internal eBGP config generated from Netbox source into netdb.

    :param test: Synchonize all devices if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.synchronize_ebgp
        salt-run netbox.synchronize_ebgp test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_netbox_util('synchronize_ebgp', test=test)


def update_ptrs(test=True):
    """
    Trigger the Netbox update_ptrs (Regularize PTR Fields) script.

    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.update_ptrs
        salt-run netbox.update_ptrs test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_netbox_util('update_ptrs', test=test)


def update_iface_descriptions(test=True):
    """
    Trigger the Netbox update_iface_descriptions (Regularize Interface Descriptions) 
    script.

    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.update_iface_descriptions
        salt-run netbox.update_iface_descriptions test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_netbox_util('update_iface_descriptions', test=test)


def renumber(ipv4, ipv6, test=True):
    """
    Trigger the Netbox renumber (Regenerate IPs renumber phase) script. Creates
    new IPs on targeted interfaces, marks old IPs for pruning.

    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.renumber ipv4='23.181.24.0/24' ipv6='2620:136:a009:df99::/64'

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    params = {
            'ipv4': ipv4,
            'ipv6': ipv6,
            }

    return _call_netbox_util('renumber', params=params, test=test)


def prune_ips(test=True):
    """
    Trigger the Netbox prune_ips (Regenerate IPs cleanup) script. Cleans up old
    IPs, regularizes new IP tags after IP generation process done.

    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.prune_ips
        salt-run netbox.prune_ips test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_netbox_util('prune_ips', test=test)
