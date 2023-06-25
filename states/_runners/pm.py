import logging, copy
from netaddr   import IPSet
from ipaddress import ip_interface, ip_network
from copy      import deepcopy

__virtualname__ = "pm"

_PM_UTIL_NAME = 'pm'

log = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__


def _call_pm_util(function, data=None, params=None, method='GET', test=True):
    endpoint = _PM_UTIL_NAME + '/' + function

    return __utils__['netdb_runner.call_netdb_util'](endpoint, data=data, params=params, method=method, test=test)


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


def set_maintenance(device, neighbor):
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
            'device' : device.upper(),
            'ip'     : neighbor,
            'status' : 'maintenance',
            }

    return _call_pm_util('set_status', params=params, method='PUT')


def set_enabled(device, neighbor):
    """
    Set a Peering Manager session to enabled and synchronize netdb.

    :param device: the device where session is located.
    :param neighbor: the neighbor IP address of the session.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.set_enabled sin2 169.254.169.254

    """
    params = {
            'device' : device.upper(),
            'ip'     : neighbor,
            'status' : 'enabled',
            }

    return _call_pm_util('set_status', params=params, method='PUT')


def create_policy(name, type, family, weight=None, comment=None):
    """
    Add a new policy to peering manager.

    :param name: the name of the new policy.
    :param type: policy type (i.e. import, export or both).
    :param family: policy family (i.e. ipv4, ipv6 or both).
    :param weight: PM policy weight
    :param comment: PM policy comment
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.create_policy 6-NEW-POLICY-IN import ipv6
        salt-run pm.create_policy 4-NEW-POLICY-OUT export ipv4 comment="new policy"

    """
    data = {
            'name'    : name,
            'type'    : type,
            'family'  : family,
            'weight'  : weight,
            'comment' : comment,
            }

    return _call_pm_util('create_policy', data=data, method='POST')


def delete_policy(name):
    """
    Delete a policy in peering manager.

    :param name: the name of the policy.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.delete_policy 6-NEW-POLICY-IN

    """
    params = {
            'name': name,
            }

    return _call_pm_util('delete_policy', params=params, method='DELETE')


def create_asn(asn, name, comment=None, ipv4_prefix_limit=None, ipv6_prefix_limit=None):
    """
    Add a new policy to peering manager.

    :param asn: the autonomous system number.
    :param name: the name of the ASN.
    :param comment: PM policy comment
    :param ipv4_prefix_limit: IPv4 prefix limit
    :param ipv6_prefix_limit: IPv6 prefix limit
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.create_asn 13335 Cloudflare "Cloudflare ASN"
        salt-run pm.create_asn 13335 Cloudflare ipv4_prefix_limit=10000

    """
    data = {
            'asn'     : asn,
            'name'    : name,
            'comment' : comment,
            'ipv4_prefix_limit' : ipv4_prefix_limit,
            'ipv6_prefix_limit' : ipv6_prefix_limit,
            }

    return _call_pm_util('create_asn', data=data, method='POST')


def peeringdb_sync_asn(asn):
    """
    Synchronize an ASN on Peering Manager from Peeringdb

    :param asn: the autonomous system number.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.peeringdb_sync_asn 13335

    """
    params = {
            'asn': asn,
            }

    return _call_pm_util('peeringdb_asn_sync', params=params, method='POST')


def add_direct_session(device, peer_ip, asn, import_policy=None, export_policy=None, local_ip=None,
                          type='transit-session', comment=None, ttl=None, status=None, local_asn=36198):
    """
    Add a new direct (i.e. non-IXP) eBGP session to peering manager.

    :param device: device where session will be installed
    :param peer_ip: IP address of eBGP peer
    :param asn: the autonomous system number.
    :param import_policy: Import policy (route-map) for the session
    :param export_policy: Export policy (route-map) for the session
    :param local_ip: Source IP address for BGP session
    :param type: Session type (e.g. transit-session or peering-session)
    :param comment: PM session comment
    :param ttl: eBGP multihop ttl
    :param status: Session status (i.e. enabled, disabled, or maintenance)
    :param local_asn: Local ASN (should normally be 36198, which is default)
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.add_direct_session mci3 181.23.71.85 20473 4-VULTR-IN 4-VULTR-OUT
        salt-run pm.add_direct_session mci3 169.254.169.254 64515 4-VULTR-IN 4-VULTR-OUT ttl=2 local_ip=139.180.130.102

    """
    data = {
            'device'    : device.upper(),
            'remote_ip' : peer_ip,
            'local_ip'  : local_ip,
            'peer_asn'  : asn,
            'import'    : import_policy,
            'export'    : export_policy,
            'type'      : type,
            'comment'   : comment,
            'ttl'       : ttl,
            'status'    : status,
            'local_asn' : local_asn,
            }

    return _call_pm_util('create_direct_session', data=data, method='POST')


def update_direct_session(device, peer_ip, import_policy=None, export_policy=None,
                                 local_ip=None,  comment=None, ttl=None, status=None):
    """
    Add a new direct (i.e. non-IXP) eBGP session to peering manager. An input
    of '0' means empty (e.g. import_policy=0 will clear the import policy).

    :param device: device where session will be installed
    :param peer_ip: IP address of eBGP peer
    :param import_policy: Import policy (route-map) for the session
    :param export_policy: Export policy (route-map) for the session
    :param local_ip: Source IP address for BGP session
    :param comment: PM session comment
    :param ttl: eBGP multihop ttl
    :param status: Session status (i.e. enabled, disabled, or maintenance)
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.update_direct_session mci3 181.23.71.85 export_policy=4-VULTR-OUT
        salt-run pm.update_direct_session mci3 181.23.71.85 import_policy=0
        salt-run pm.update_direct_session mci3 169.254.169.254 comment="Vultr Session" ttl=2

    """
    data = {
            'device'    : device.upper(),
            'remote_ip' : peer_ip,
            'local_ip'  : local_ip,
            'import'    : import_policy,
            'export'    : export_policy,
            'comment'   : comment,
            'ttl'       : ttl,
            'status'    : status,
            }

    return _call_pm_util('update_direct_session', data=data, method='PUT')


def delete_direct_session(device, neighbor):
    """
    Delete a direct session in peering manager and
    synchronize netdb.

    :param device: the device where session is located.
    :param neighbor: the neighbor IP address of the session.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if successful; false otherwise
       * out: a dict of synchronization results

    CLI Example::

    .. code-block:: bash

        salt-run pm.delete_direct_session mci3 169.254.169.254

    """
    params = {
            'device' : device.upper(),
            'ip'     : neighbor,
            }

    return _call_pm_util('delete_direct_session', params=params, method='DELETE')
