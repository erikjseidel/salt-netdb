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


def _call_netbox_util(function, data=None, test=True):
    endpoint = _NETBOX_UTIL_NAME + '/' + function

    return __utils__['netdb_runner.call_netdb_util'](endpoint, data=data, test=test)


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
