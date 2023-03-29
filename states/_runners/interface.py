# -*- coding: utf-8 -*-

import logging, json, re
from ipaddress import ip_interface
from copy import deepcopy

__virtualname__ = "interface"

log = logging.getLogger(__file__)

_COLUMN = 'interface'

def __virtual__():
    return __virtualname__


def _netdb_save(data, test):
    return __utils__['netdb_runner.save'](_COLUMN, data, test)


def _netdb_update(data, test):
    return __utils__['netdb_runner.update'](_COLUMN, data, test)


def _netdb_delete(data, test):
    return __utils__['netdb_runner.delete'](_COLUMN, data, test)


def _netdb_get(data):
    return __utils__['netdb_runner.get'](_COLUMN, data = data)


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

        salt-run interface.get sin3 tun376
        salt-run interface.get interface=tun376

    """
    if device:
        device = device.upper()
    filt = [ device, None, None, interface ]
    netdb_answer = _netdb_get(filt)

    return netdb_answer


def add_addr(device, interface, address, ptr = None, roles = None, test = True):
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

        salt-run interface.get sin3 tun376
        salt-run interface.get interface=tun376

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    try:
        ip_interface(address)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid IP address' }

    device = device.upper()
    filt = [ device, None, None, interface ]
    netdb_answer = _netdb_get(filt)

    if not netdb_answer['result']:
        return netdb_answer

    data = netdb_answer['out']
    iface = data[device]['interfaces'][interface]

    if 'address' not in iface:
        iface['address'] = {}
    elif address in iface['address'].keys():
        return { 'result': False, 'error': True, 'comment': 'This IP address is already assigned to %s' % interface }

    iface['address'][address] = None

    if ptr or roles:
        iface['address'][address] = { 'meta': {} }
        if ptr:
            iface['address'][address]['meta']['dns'] = { 'ptr': ptr }
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

        salt-run interface.get sin3 tun376
        salt-run interface.get interface=tun376

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    try:
        ip_interface(address)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid IP address' }

    device = device.upper()
    filt = [ device, None, None, interface ]
    netdb_answer = _netdb_get(filt)

    if not netdb_answer['result']:
        return netdb_answer

    data = netdb_answer['out']
    iface = data[device]['interfaces'][interface]

    if 'address' not in iface or address not in iface['address']:
        return { 'result': False, 'error': True, 'comment': 'No such IP address assigned to %s' % interface }

    iface['address'].pop(address, None)

    return _netdb_update(data, test)


def update_addr(device, interface, address, ptr = None, roles = None, new_addr = None, test = True):
    """
    Update an IP address to an interface.

    :param device: device where interface is located
    :param interface: interface to which the new address is to be added
    :param address: address to be updated
    :param ptr: new dns ptr record to be associated with this address (set 'empty' to delete)
    :param roles: a comma separated list of address roles (set 'empty' to delete)
    :param new_addr: a new address (i.e. change the address itself)
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt-run interface.update sin3 tun376 23.181.64.76/31 roles=decom,l3ptp
        salt-run interface.update sin3 tun376 23.181.64.76/31 ptr=empty
        salt-run interface.update sin3 tun376 23.181.64.76/31 new_addr=23.181.64.126/31

    """
    if not new_addr and not roles and not ptr:
        return { 'result': False, 'error': True, 'comment': 'Nothing to update' }

    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    try:
        ip_interface(address)
        if new_addr:
            ip_interface(new_addr)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid IP address' }

    device = device.upper()
    filt = [ device, None, None, interface ]
    netdb_answer = _netdb_get(filt)

    if not netdb_answer['result']:
        return netdb_answer

    data = netdb_answer['out']
    iface = data[device]['interfaces'][interface]

    if 'address' in iface.keys() and address in iface['address'].keys():
        update = deepcopy(iface['address'][address])
    else:
        return { 'result': False, 'error': True, 'comment': 'This IP address not found on %s' % interface }

    if ptr or roles:
        if 'meta' not in update:
            update = { 'meta': {} }
        if ptr:
            if 'dns' not in update['meta']:
                update['meta']['dns'] = {}
            if ptr.lower() == 'empty':
                update['meta'].pop('dns', None)
            else:
                update['meta']['dns']['ptr'] = ptr
        if roles:
            if roles.lower() == 'empty':
                update['meta'].pop('role', None)
            else:
                update['meta']['role'] = roles.split(',')

    iface['address'].pop(address, None)
    
    if new_addr:
        address = new_addr

    iface['address'][address] = update

    return _netdb_update(data, test)


def enable(device, interface, test = True):
    """
    Remove the disabled mark from an interface. State must be applied in
    order to activate. If you wish to disable without applying state please
    run the corresponding disable module on the device's proxy minion.

    :param device: device where interface is located
    :param interface: interface to do be enabled
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt-run interface.enable sin3 tun376
        salt-run interface.enable device=sin3 interface=tun376

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    device = device.upper()
    filt = [ device, None, None, interface ]
    netdb_answer = _netdb_get(filt)

    if not netdb_answer['result']:
        return netdb_answer

    data = netdb_answer['out']
    data[device]['interfaces'][interface].pop('disabled', None)

    return _netdb_update(data, test)


def disable(device, interface, test = True):
    """
    Mark an interface as disabled. State must be applied in order to
    activate. If you wish to disable without applying state please run
    the corresponding disable module on the device's proxy minion.

    :param device: device where interface is located
    :param interface: interface to be disabled
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt-run interface.disable sin3 tun376
        salt-run interface.disable device=sin3 interface=tun376

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    device = device.upper()
    filt = [ device, None, None, interface ]
    netdb_answer = _netdb_get(filt)

    if not netdb_answer['result']:
        return netdb_answer

    data = netdb_answer['out']
    data[device]['interfaces'][interface]['disabled'] = True

    return _netdb_update(data, test)


def add_tunnel(device, tunnel, description=None, type='gre', 
        source=None, remote=None, interface=None, mtu=None, ttl=64, test=True):
    """
    Add a tunnel interface to a device.

    :param device: device where interface is to be added
    :param interface: interface to be added
    :param description: an interface description (optional)
    :param type: tunnel interface type (required, gre or l2gre)
    :param source: source IP address for encapsulated packets (optional)
    :param remote: remote (i.e. peer) IP address (required)
    :param interface: parent interface for tunnel (optional)
    :param mtu: tunnel mtu (optional)
    :param ttl: tunnel ttl (default 64)
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt-run interface.add_tunnel sin1 tun390 interface='eth1' remote=1.1.1.1 mtu=1450
        salt-run interface.add_tunnel sin1 tun390 remote=1.1.1.1 mtu=1450 test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    tun_name = re.compile("^((tun)([0-9]{3}|[0-9]{2}|[0-9]{1}))*$")
    if_name  = re.compile("^((dum|eth|bond)([0-9]{3}|[0-9]{2}|[0-9]{1}))*$")

    if not tun_name.match(tunnel):
        return { 'result': False, 'error': True, 'comment': 'Invalid tunnel name' }
    if interface and not if_name.match(interface):
        return { 'result': False, 'error': True, 'comment': 'Invalid interface name' }

    if not remote:
        return { 'result': False, 'error': True, 'comment': 'remote required for tunnel interfaces' }

    try:
        if source:
            ip_interface(source)
        if remote:
            ip_interface(remote)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid IP address' }

    if not type or type not in ['gre', 'l2gre']:
        return { 'result': False, 'error': True, 'comment': 'Invalid tunnel type. Must be gre or l2gre' }
    if ttl and int(ttl) not in range(1, 255):
        return { 'result': False, 'error': True, 'comment': 'ttl must be between 1 and 255' }
    if mtu and int(mtu) not in range(576, 9172):
        return { 'result': False, 'error': True, 'comment': 'mtu must be between 576 and 9172' }

    device = device.upper()
    filt = [ device, None, None, tunnel ]
    netdb_answer = _netdb_get(filt)

    if ( 'out'        in netdb_answer and
         device       in netdb_answer['out'] and
         'interfaces' in netdb_answer['out'][device] and
         tunnel       in netdb_answer['out'][device]['interfaces']):
        return { 'result': False, 'comment': 'Interface already exists' }

    tun = { 'type': type }

    if description:
        tun['description'] = description
    if source:
        tun['source'] = source
    if remote:
        tun['remote'] = remote
    if interface:
        tun['interface'] = interface
    if mtu:
        tun['mtu'] = mtu
    if ttl:
        tun['ttl'] = ttl

    data = { device: { 'interfaces': { tunnel : tun } } }

    return _netdb_save(data, test)


def delete(device, interface, test=True):
    """
    Delete an interface.

    :param device: device where interface is located
    :param interface: interface to be deleted
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt-run interface.delete sin3 tun376 test=false
        salt-run interface.delete device=sin3 interface=tun376

    """

    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    device = device.upper()
    filt = [ device, None, None, interface ]
    netdb_answer = _netdb_get(filt)

    if not netdb_answer['result']:
        return netdb_answer

    ret = _netdb_delete(filt, test)
    ret.update({ 'out': netdb_answer['out'] })

    return ret
