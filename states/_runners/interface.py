# -*- coding: utf-8 -*-

import logging, json, re
from functools import wraps
from ipaddress import ip_interface, IPv4Address
from copy import deepcopy

__virtualname__ = "interface"

log = logging.getLogger(__file__)

_COLUMN = 'interface'

# Supported vyos if types
_VYOS_VLAN  = "^(eth|bond)([0-9]{1,3})(\.)([0-9]{1,4})$"
_VYOS_ETH   = "^(eth)([0-9]{1,3})$"
_VYOS_LAG   = "^(bond)([0-9]{1,3})$"
_VYOS_TUN   = "^(tun)([0-9]{1,3})$"
_VYOS_DUM   = "^(dum)([0-9]{1,3})$"

_TYPE_DICT = {
        'eth'    :  re.compile(_VYOS_ETH),
        'gre'    :  re.compile(_VYOS_TUN),
        'l2gre'  :  re.compile(_VYOS_TUN),
        'vlan'   :  re.compile(_VYOS_VLAN),
        'lacp'   :  re.compile(_VYOS_LAG),
        'dummy'  :  re.compile(_VYOS_DUM),
        }

# Used to verify parent interfaces for tunnels
_VYOS_PARENT  = "^(eth|bond)([0-9]{1,3})(?:(\.)([0-9]{1,4})){0,1}$"

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


def _testable(func):
    """
    Checks if test is type bool.
    """
    @wraps(func)
    def decorator(*args, test=True, **kwargs):
        if not isinstance(test, bool):
            return {"result": False, "comment": "test only accepts true or false."}

        kwargs.update({ 'test': test })
        return func(*args, **kwargs)
    return decorator


def _netdb_interface(func):
    """
    For extant interfaces: Queries the device / interface pair from netdb.

    Sends the data to child function if found. Returns the netdb api error
    message otherwise.
    """
    @_testable
    @wraps(func)
    def decorator(*args, Test=True, **kwargs):
        args = list(args)
        args[0] = args[0].upper()  # args[0] is the device; args[1] is the interface

        filt = [ args[0], None, None, args[1] ]
        netdb_answer = _netdb_get(filt)

        if not netdb_answer['result']:
            netdb_answer.update({ 'comment': '%s: Interface not found' % args[1] })
            return netdb_answer

        kwargs.update({ 'data': netdb_answer['out'] })
        return func(*args, **kwargs)
    return decorator


def _validator(func):
    """
    Wrapper around validator functions to enforce proper interface
    """
    def decorator(*args, **kwargs):
        result, comment = func(*args, **kwargs)

        if result:
            return { 'result': True, 'error': False }

        return { 'result': False, 'error': True, 'comment': comment }
    return decorator


def _interface_check(device, interface):
    """
    Returns True if the device / interface pair exists; False otherwise
    """
    filt = [ device, None, None, interface ]
    if _netdb_get(filt)['result']:
        return True

    return False


def _get_interface_type(interface):
    # Won't be a perfect match in case of tunnels but as attributes are
    # the same it should not be a problem.
    for if_type in _TYPE_DICT.keys():
        if _TYPE_DICT[if_type].match(interface):
            return if_type

    return None


@_validator
def _common_options_checker(interface, type, description, mtu):
    """
    Validate arguments used by all interface types.
    """
    if type not in _TYPE_DICT.keys():
        return False, 'Invalid interface type. Please see documentation for supported types.'

    if not _TYPE_DICT[type].match(interface):
        return False, 'Interface name incompatable with interface type.'

    if description and (not isinstance(description, str) or len(description) > 100):
        return False, 'Interface description must be a string of 100 characters or less.'

    if mtu and mtu not in range(576, 9173):
        return False, 'Interface MTU must be between 576 and 9172.'

    return True, None


@_validator
def _tunnel_options_checker(remote, source, ttl, parent, key):
    """
    Validate arguments used by the tunnel interface types (i.e. gre and l2gre)
    """
    try:
        ip_interface(remote)
    except:
        return False, 'Invalid tunnel remote IP address'

    try:
        if source:
            ip_interface(source)
    except:
        return False, 'Invalid tunnel source IP address'

    if ttl and int(ttl) not in range(1, 256):
        return False, 'ttl must be between 1 and 255'

    if parent and not re.compile(_VYOS_PARENT).match(parent):
        return False, 'Invalid parent interface name'

    try:
        if key:
            IPv4Address(key)
    except:
        return False, 'Invalid tunnel key value'

    return True, None


@_validator
def _lacp_options_checker(lacp_hash, lacp_members, lacp_min_links, lacp_rate):
    """
    Validate arguments used by the lacp (i.e. bond / lag bundle in lacp mode) interface type
    """

    if not lacp_hash or lacp_hash not in ['layer2+3', 'layer3+4']:
        return False, 'Invalid LACP hash. Must be "layer2+3" or "layer3+4"'

    if not isinstance(lacp_members, list) or len(lacp_members) not in range(1, 6):
        return False, 'LACP interface must have between 1 and 5 member ports'

    if not lacp_min_links or int(lacp_min_links) < 1:
        return False, 'LACP interface min links cannot be less than one'

    if not lacp_rate or lacp_rate not in ['fast', 'slow']:
        return False, 'LACP rate must be either "fast" or "slow"'

    return True, None


@_validator
def _vlan_check(vlan):
    """
    Checks the validity of vlan interfaces.
    """
    if ( _TYPE_DICT['vlan'].match(vlan) and
            int(vlan.split('.')[1]) in range(1, 4096) ):
        return False, '%s: vlan id must be between 1 and 4095.' % interface

    return True, None


def get(device=None, interface=None):
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


@_netdb_interface
def add_addr(device, interface, address, ptr=None, roles=None, test=True, data=None):
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
    try:
        ip_interface(address)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid IP address' }

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


@_netdb_interface
def delete_addr(device, interface, address, test=True, data=None):
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
    try:
        ip_interface(address)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid IP address' }

    iface = data[device]['interfaces'][interface]

    if 'address' not in iface or address not in iface['address']:
        return { 'result': False, 'error': True, 'comment': 'No such IP address assigned to %s' % interface }

    iface['address'].pop(address, None)

    return _netdb_update(data, test)


@_netdb_interface
def update_addr(device, interface, address, ptr=None, roles=None, new_addr=None, test=True, data=None):
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

    try:
        ip_interface(address)
        if new_addr:
            ip_interface(new_addr)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid IP address' }

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
    
    if new_addr: address = new_addr

    iface['address'][address] = update

    return _netdb_update(data, test)


@_netdb_interface
def set_firewall(device, interface, ipv6_local=None, ipv4_local=None,
        ipv6_ingress=None, ipv4_ingress=None, ipv6_egress=None, ipv4_egress=None, test=True, data=None):
    """
    Set firewall policies for an interface. Defaults to no change.
    Setting 'disable' will remove an existing policy.

    :param device: device where source interface is located
    :param interface: source interface to be copied 
    :param ipv6_local: sets local ipv6 firewall policy
    :param ipv4_local: sets local ipv4 firewall policy
    :param ipv6_ingress: sets ingress ipv6 firewall policy
    :param ipv4_ingress: sets ingress ipv4 firewall policy
    :param ipv6_egress: sets egress ipv6 firewall policy
    :param ipv4_egress: sets egress ipv4 firewall policy
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt-run interface.set_firewall sin3 tun376 ipv4_local=disable ipv6_egress=NEW_POLICY
        salt-run interface.set_firewall sin3 tun376 ipv4_egress=4TEST ipv6_egress=6TEST

    """
    rule_dict = {
            'local'   :  { 'ipv6' : ipv6_local,   'ipv4': ipv4_local   },
            'ingress' :  { 'ipv6' : ipv6_ingress, 'ipv4': ipv4_ingress },
            'egress'  :  { 'ipv6' : ipv6_egress,  'ipv4': ipv4_egress  },
            }

    iface = data[device]['interfaces'][interface]

    if 'firewall' not in iface:
        iface['firewall'] = {}

    def update_firewall(policy, family, name):
        if name:
            if policy not in iface['firewall']: iface['firewall'][policy] = {}

            if name == 'disable':
                iface['firewall'][policy].pop(family, None)
            elif isinstance(name, str):
                iface['firewall'][policy][family] = name
            elif name:
                return False, 'Invalid %s %s ruleset name.' % (family, policy)

        return True, None

    for group in ['local', 'ingress', 'egress']:
        for fam in ['ipv6', 'ipv4']:
            result, message = update_firewall(group, fam, rule_dict[group][fam])
            if not result:
                return { 'result': False, 'comment': message }

    return _netdb_update(data, test)


@_netdb_interface
def enable(device, interface, test=True, data=None):
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
    data[device]['interfaces'][interface].pop('disabled', None)

    return _netdb_update(data, test)


@_netdb_interface
def disable(device, interface, test=True, data=None):
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
    data[device]['interfaces'][interface]['disabled'] = True

    return _netdb_update(data, test)


@_testable
def add(device, interface, description=None, type='eth', mtu=None, 
        lacp_hash=None, lacp_members=None, lacp_min_links=None, lacp_rate=None,
        source=None, remote=None, tunnel_parent=None, ttl=None, key=None, test=True):
    """
    Add an interface to a device.

    :param device: device where interface is to be added
    :param interface: interface to be added
    :param description: an interface description (optional)
    :param type: interface type (required, eth, vlan, lacp, dummy, gre, l2gre)
    :param mtu: interface mtu (optional)
    :param lacp_hash: (LACP) hash for lacp; either 'layer2+3' or 'layer3+4'
    :param lacp_members: (LACP) comma separated list of lacp member ports
    :param lacp_min_links: (LACP) minimum up ports required by the bundle
    :param lacp_rate: (LACP) pdu signaling rate; either 'fast' or 'slow'
    :param source: (tunnels) source IP address for encapsulated packets (optional)
    :param remote: (tunnels) remote (i.e. peer) IP address (required)
    :param tunnel_parent: (tunnels) parent interface for tunnel (optional)
    :param ttl: (tunnels) outer packet ttl (default 64)
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt-run interface.add sin1 tun390 interface='eth1' remote=1.1.1.1 mtu=1450
        salt-run interface.add sin1 tun390 remote=1.1.1.1 mtu=1450 test=false

    """
    ret = _common_options_checker(interface, type, description, mtu)
    if ret['error']: return ret

    if type in ['gre', 'l2gre']:
        ret = _tunnel_options_checker(remote, source, ttl, tunnel_parent, key)
        if ret['error']: return ret

    elif any([source, remote, tunnel_parent, ttl, key]):
        return {'result': False, 'comment': 'source, remote, tunnel_parent, ttl, key are for tunnels only' }

    if type == 'lacp':
        if isinstance(lacp_members, str): lacp_members = lacp_members.split(',')
        ret = _lacp_options_checker(lacp_hash, lacp_members, lacp_min_links, lacp_rate)
        if ret['error']: return ret

    elif any([lacp_hash, lacp_members, lacp_min_links, lacp_rate]):
        return {'result': False, 'comment': 'lacp* arguments can only be used with lacp/lag type' }

    if type == 'vlan':
        ret = _vlan_check(interface)
        if ret['error']: return ret

    if type == 'eth':
        type = 'ethernet'

    device = device.upper()
    if _interface_check(device, interface):
        return { 'result': False, 'comment': 'Interface already exists' }

    new = { 'type': type }

    if description:
        new['description'] = description
    if mtu:
        new['mtu'] = mtu

    if type == 'vlan':
        new['vlan'] = {
                'parent' : interface.split('.')[0],
                'id'     : interface.split('.')[1],
                }

    if type == 'lacp':
        new['lacp'] = {
                'hash_policy' : lacp_hash,
                'members'     : lacp_members,
                'min_links'   : lacp_min_links,
                'rate'        : lacp_rate,
                }

    if type in ['gre', 'l2gre']:
        if source:
            new['source'] = source
        if remote:
            new['remote'] = remote
        if interface:
            new['interface'] = interface
        if ttl:
            new['ttl'] = ttl

    data = { device: { 'interfaces': { interface : new } } }

    return _netdb_save(data, test)


@_netdb_interface
def modify(device, interface, description=None, mtu=None,
        lacp_hash=None, lacp_members=None, lacp_min_links=None, lacp_rate=None,
        source=None, remote=None, tunnel_parent=None, ttl=None, key=None, test=True, data=None):
    """
    Add an interface to a device.

    :param device: device where interface is to be added
    :param interface: interface to be added
    :param description: an interface description (optional)
    :param mtu: interface mtu (optional)
    :param lacp_hash: (LACP) hash for lacp; either 'layer2+3' or 'layer3+4'
    :param lacp_members: (LACP) comma separated list of lacp member ports
    :param lacp_min_links: (LACP) minimum up ports required by the bundle
    :param lacp_rate: (LACP) pdu signaling rate; either 'fast' or 'slow'
    :param source: (tunnels) source IP address for encapsulated packets (optional)
    :param remote: (tunnels) remote (i.e. peer) IP address (required)
    :param tunnel_parent: (tunnels) parent interface for tunnel (optional)
    :param ttl: (tunnels) outer packet ttl (default 64)
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt-run interface.modify sin1 tun390 interface='eth1' remote=1.1.1.1 mtu=1450
        salt-run interface.modify sin1 tun390 remote=1.1.1.1 mtu=1450 test=false

    """
    type = _get_interface_type(interface)

    ret = _common_options_checker(interface, type, description, mtu)
    if ret['error']: return ret

    if type in ['gre', 'l2gre']:
        ret = _tunnel_options_checker(remote, source, ttl, tunnel_parent, key)
        if ret['error']: return ret

    elif any([source, remote, tunnel_parent, ttl, key]):
        return {'result': False, 'comment': 'source, remote, tunnel_parent, ttl, key are for tunnels only' }

    if type == 'lacp':
        if isinstance(lacp_members, str): lacp_members = lacp_members.split(',')
        ret = _lacp_options_checker(lacp_hash, lacp_members, lacp_min_links, lacp_rate)
        if ret['error']: return ret

    elif any([lacp_hash, lacp_members, lacp_min_links, lacp_rate]):
        return {'result': False, 'comment': 'lacp* arguments can only be used with lacp/lag type' }

    if type == 'eth':
        type = 'ethernet'

    iface = data[device]['interfaces'][interface]

    if description:
        iface['description'] = description
    if mtu:
        iface['mtu'] = mtu

    if type == 'lacp':
        iface['lacp'] = {
                'hash_policy' : lacp_hash,
                'members'     : lacp_members,
                'min_links'   : lacp_min_links,
                'rate'        : lacp_rate,
                }

    if type == 'tunnel':
        if source:
            iface['source'] = source
        if remote:
            iface['remote'] = remote
        if interface:
            iface['interface'] = interface
        if ttl:
            iface['ttl'] = ttl

    data = { device: { 'interfaces': { interface : iface } } }

    return _netdb_update(data, test)


@_netdb_interface
def copy(device, interface, new_dev, new_int, test=True, data=None):
    """
    Copy an interface. New interface will have all the same
    attributes as the original. Interface type must match for this
    operation to succeed.

    :param device: device where source interface is located
    :param interface: source interface to be copied 
    :param new_dev: device where new interface is to be located
    :param new_int: new (i.e. destination) interface
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise
       * out: dict containing updated interface and attributes

    CLI Example::

    .. code-block:: bash

        salt-run interface.copy sin3 tun376 sin1 tun390
        salt-run interface.copy sin3 tun376 sin1 tun390 test=false

    """
    if_type = _get_interface_type(interface)

    if not if_type:
        return {'result': False, 'comment': '%s: unsupported interface type.' % interface }

    if not _TYPE_DICT[if_type].match(new_int):
        return {'result': False, 'comment': '%s: source and target interface must be the same type.' % new_int }

    if if_type == 'vlan':
        ret = _vlan_check(new_int)
        if ret['error']: return ret

    new_dev = new_dev.upper()
    if _interface_check(new_dev, new_int):
        return { 'result': False, 'comment': '%s says: Interface already exists' % new_dev }

    data[new_dev] = data.pop(device)
    data[new_dev]['interfaces'][new_int] = data[new_dev]['interfaces'].pop(interface)

    # the case of vlan copies correct the vlan id and parent interface.
    if if_type == 'vlan':
        data[new_dev]['interfaces'][new_int]['vlan'] = {
                'id'     : int(new_int.split('.')[1]),
                'parent' : new_int.split('.')[0],
                }

    return _netdb_save(data=data, test=test)


@_netdb_interface
def delete(device, interface, test=True, data=None):
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
    filt = [ device, None, None, interface ]

    ret = _netdb_delete(filt, test)
    ret.update({ 'out': data })

    return ret
