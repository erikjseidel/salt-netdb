import logging, copy
from netaddr   import IPSet
from ipaddress import ip_interface, ip_network
from copy      import deepcopy

__virtualname__ = "netbox"

_NETBOX_UTIL_EP = 'connectors/netbox'

log = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__


def _call_netbox_util(function, data=None, params=None, method='GET', test=True):
    endpoint = f'{_NETBOX_UTIL_EP}/{function}'

    return __utils__['netdb_util.call_netdb_util'](endpoint, data=data, params=params, method=method, test=test)


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
    return _call_netbox_util('device')


def generate_interfaces():
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
    return _call_netbox_util('interface')


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
    return _call_netbox_util('igp')


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
    return _call_netbox_util('ebgp')


def reload_devices(verbose=False):
    """
    Clear all Netbox data from netdb device column and load
    a fresh version from Netbox

    :param verbose: show generated column data as well
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of devices in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run netbox.reload_devices

    """
    ret = _call_netbox_util('device', method='POST')

    if ret['result'] and not ret['error'] and not verbose:
        return { 'result': True }

    return ret


def reload_interfaces(verbose=False):
    """
    Clear all Netbox data from netdb interface column and load
    a fresh version from Netbox

    :param verbose: show generated column data as well
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of interfaces in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run netbox.reload_interfaces

    """
    ret = _call_netbox_util('interface', method='POST')

    if ret['result'] and not ret['error'] and not verbose:
        return { 'result': True }

    return ret


def reload_isis(verbose=False):
    """
    Clear all Netbox data from netdb bgp column and load
    a fresh version from Netbox

    :param verbose: show generated column data as well
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of IS-IS data in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run netbox.reload_isis

    """
    ret = _call_netbox_util('igp', method='POST')

    if ret['result'] and not ret['error'] and not verbose:
        return { 'result': True }

    return ret


def reload_bgp(verbose=False):
    """
    Clear all Netbox data from netdb bgp column and load
    a fresh version from Netbox

    :param verbose: show generated column data as well
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of BGP data in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run netbox.reload_bgp

    """
    ret = _call_netbox_util('ebgp', method='POST')

    if ret['result'] and not ret['error'] and not verbose:
        return { 'result': True }

    return ret


def update_ptrs(test=True):
    """
    Trigger the Netbox update_ptrs (Regularize PTR Fields) script.

    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of script run results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.update_ptrs
        salt-run netbox.update_ptrs test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_netbox_util('script/update_ptrs', method='POST', test=test)


def update_iface_descriptions(test=True):
    """
    Trigger the Netbox update_iface_descriptions (Regularize Interface Descriptions) 
    script.

    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of script run results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.update_iface_descriptions
        salt-run netbox.update_iface_descriptions test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_netbox_util('script/update_iface_descriptions', method='POST', test=test)


def renumber(ipv4, ipv6, test=True):
    """
    Trigger the Netbox renumber (Regenerate IPs renumber phase) script. Creates
    new IPs on targeted interfaces, marks old IPs for pruning.

    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of script run results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.renumber ipv4='23.181.24.0/24' ipv6='2620:136:a009:df99::/64'

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    data = {
            'ipv4_prefix': ipv4,
            'ipv6_prefix': ipv6,
            }

    return _call_netbox_util('script/renumber', data=data, method='POST', test=test)


def prune_ips(test=True):
    """
    Trigger the Netbox prune_ips (Regenerate IPs cleanup) script. Cleans up old
    IPs, regularizes new IP tags after IP generation process done.

    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of script run results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.prune_ips
        salt-run netbox.prune_ips test=false

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return _call_netbox_util('script/prune_ips', method='POST', test=test)


def create_pni(device, interface, peer_name, cid, test=True):
    """
    Trigger the Netbox add_pni (create a new PNI) script. Creates new IPs on the
    interface as well. Sub-interfaces for VLAN tagged PNIs will be dynamically
    created.

    :param device: Device where PNI is located
    :param interface: Interface name of the PNI
    :param peer_name: Name of PNI Peer (netbox Provider)
    :param cid: Circuit ID
    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of script run results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.create_pni sin1 eth5 Acme cid=ACM001 test=false
        salt-run netbox.create_pni sin1 eth5 Acme ACM001

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    data = {
            'device'     : device.upper(),
            'interface'  : interface,
            'peer_name'  : peer_name,
            'circuit_id' : cid,
            }

    data = { k : v for k, v in data.items() if v }

    return _call_netbox_util('script/create_pni', data=data, method='POST', test=test)


def create_bundle(device, interfaces, layer3_4=False, lacp_slow=False, test=True):
    """
    Trigger the Netbox add_pni (create a new PNI) script. Creates new IPs on the
    interface as well. Sub-interfaces for VLAN tagged PNIs will be dynamically
    created.

    :param device: Device where PNI is located
    :param interfaces: Interfaces to be included in the bundle (comma separated list)
    :param layer3_4: True to enable layer3+4 hashing (non-standard)
    :param lacp_slow: True to enable LACP slow rate
    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of script run results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.create_bundle sin1 eth4,eth5 test=false
        salt-run netbox.create_bundle sin1 eth5 layer3_4=true

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    if not isinstance(layer3_4, bool):
        return {"result": False, "comment": "layer3_4 only accepts true or false."}

    if not isinstance(lacp_slow, bool):
        return {"result": False, "comment": "lacp_slow only accepts true or false."}

    if not isinstance(interfaces, str):
        return {"result": False, "comment": "interfaces must be a comma separated list"}

    data = {
            'device'     : device.upper(),
            'interfaces' : interfaces.split(','),
            'layer3_4'   : layer3_4,
            'lacp_slow'  : lacp_slow,
            }

    data = { k : v for k, v in data.items() if v }

    return _call_netbox_util('script/create_bundle', data=data, method='POST', test=test)


def configure_pni(device, interface, peer_asn, vlan_id=None, vcid=None, autogen_ips=False, ipv4=None, ipv6=None, test=True):
    """
    Trigger the Netbox add_pni (create a new PNI) script. Creates new IPs on the
    interface as well. Sub-interfaces for VLAN tagged PNIs will be dynamically
    created.

    :param device: Device where PNI is located
    :param interface: Interface name of the PNI
    :param peer_asn: ASN of PNI / vPNI peer
    :param vlan_id: 802.1Q VLAN tag (if any)
    :param vcid: "Virtual" circuit ID (for VLANs, optional)
    :param autogen_ips: Automatically assign IPv4 /31 and IPv6 /127 from PNI IP pool
    :param ipv4: Manually assign IPv4 address (not used if autogen_ips set)
    :param ipv6: Manually assign IPv6 address (not used if autogen_ips set)
    :param test: Commit changes to Netbox if false, only do a dry run if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of script run results

    CLI Example::

    .. code-block:: bash

        salt-run netbox.configure_pni sin1 eth5 13335 vlan_id=650 vcid=CF001 autogen_ips=false test=false
        salt-run netbox.configure_pni sin1 eth5 13335 ipv4=23.181.24.96/31 ipv6=2620:136:a009:df99::2/127

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    data = {
            'device'             : device.upper(),
            'interface'          : interface,
            'vlan_id'            : vlan_id,
            'virtual_circuit_id' : vcid,
            'peer_asn'           : peer_asn,
            'autogen_ips'        : autogen_ips,
            'my_ipv4'            : ipv4,
            'my_ipv6'            : ipv6,
            }

    data = { k : v for k, v in data.items() if v }

    return _call_netbox_util('script/configure_pni', data=data, method='POST', test=test)
