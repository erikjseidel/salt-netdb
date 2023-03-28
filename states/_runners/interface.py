# -*- coding: utf-8 -*-

import logging, copy, json
from ipaddress import ip_interface

__virtualname__ = "interface"

log = logging.getLogger(__file__)

_COLUMN = 'interface'

def __virtual__():
    return __virtualname__


def _netdb_update(data, test=True):
    """
    This needs to be moved to util.

    """
    if not test:
        netdb_answer = __utils__['netdb_runner.request'](_COLUMN, data = data, method='PUT')
        if netdb_answer['result']:
            netdb_answer.update({'out': data})
            return netdb_answer
        else:
            return netdb_answer

    return { 'result': False, 'comment': 'Test run. Database not updated.', 'out': data }


def get(device = None, interface = None):
    """
    Show salt managed interfaces filtered by device and/or interface name.

    :param device: device to filter by.
    :param interface: interface to filter by.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: dict containing matching interfaces and their attributes

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy interface.get sin3 tun376
        salt sin1-proxy interface.get interface=tun376

    """
    filt = [ device.upper(), None, None, interface ]
    netdb_answer = __utils__['netdb_runner.request'](_COLUMN, data = filt, method='GET')

    return netdb_answer


def new_addr(device, interface, address, ptr = None, roles = None, test = True):
    """
    Add an IP address to an interface.

    :param device: device where interface is located
    :param interface: interface to which the new address is to be added
    :param ptr: dns ptr record to be associated with new address
    :param roles: a comma separated list of address roles (currently arbitrary)
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy interface.get sin3 tun376
        salt sin1-proxy interface.get interface=tun376

    """
    device = device.upper()
    filt = [ device, None, None, interface ]
    netdb_answer = __utils__['netdb_runner.request'](_COLUMN, data = filt, method='GET')

    if not netdb_answer['result']:
        return netdb_answer

    try:
        ip_interface(address)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid IP address' }

    data = netdb_answer['out']
    iface = data[device]['interfaces'][interface]

    if 'address' not in iface:
        iface['address'] = {}
    elif address in iface['address'].keys():
        return { 'result': False, 'error': True, 'comment': 'This IP address is already assigned to %s' % interface }

    iface['address'][address] = None

    if ptr or roles:
        iface['address'][address] = {}
        iface['address'][address]['meta'] = {}
        if ptr:
            iface['address'][address]['meta']['dns'] = {}
            iface['address'][address]['meta']['dns']['ptr'] = ptr
        if roles:
            iface['address'][address]['meta']['role'] = roles.split(',')

    return _netdb_update(data, test)


def delete_addr(device, interface, address, test = True):
    """
    Delete an IP address from an interface.

    :param device: device where interface is located
    :param interface: interface from which the new address is to be removed 
    :param address: address to be removed 
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy interface.get sin3 tun376
        salt sin1-proxy interface.get interface=tun376

    """
    device = device.upper()
    filt = [ device, None, None, interface ]
    netdb_answer = __utils__['netdb_runner.request'](_COLUMN, data = filt, method='GET')

    if not netdb_answer['result']:
        return netdb_answer

    try:
        ip_interface(address)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid IP address' }

    data = netdb_answer['out']
    iface = data[device]['interfaces'][interface]

    if 'address' not in iface or address not in iface['address']:
        return { 'result': False, 'error': True, 'comment': 'No such IP address assigned to %s' % interface }

    iface['address'].pop(address, None)

    return _netdb_update(data, test)
