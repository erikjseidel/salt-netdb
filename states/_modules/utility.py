import logging
import json
from netaddr import IPAddress
from netaddr.core import AddrFormatError

from net_types.salt import salt_dict_return

__virtualname__ = "utility"

logger = logging.getLogger(__file__)


def __virtual__():
    return __virtualname__


def bgp_session_check(neighbor_ip: str) -> dict:
    """
    Check the state of a BGP session.

    :param neighbor_ip: Neighbour IP address
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if session check completes; false otherwise
       * out: Test result and details

    CLI Example::

    .. code-block:: bash

        salt sin2 utility.bgp_session_check 23.181.64.98

    """
    try:
        family = 'ipv6' if IPAddress(neighbor_ip).version == 6 else 'ip'

    except AddrFormatError:
        return salt_dict_return(comment='Invalid IP address input')

    command = f'show {family} bgp neighbor {neighbor_ip} | match "BGP state"'

    ret = __salt__['net.cli'](command)
    if not ret['result']:
        return salt_dict_return(comment='net.cli false return', out=ret)

    if p := ret['out'][command]:
        state = p.split(',')[0].split(' = ')[1].upper()

    else:
        return salt_dict_return(comment='BGP sessions not found', out=ret['out'])

    return salt_dict_return(
        result=True,
        comment='BGP session check results',
        out={
            'session_out': ret['out'],
            'state': state,
            'established': (state == 'ESTABLISHED'),
        },
    )


def get_config() -> dict:
    """
    Get VyOS config in native jsonified format
    """

    return salt_dict_return(
        result=True,
        out=json.loads(
            __salt__['napalm.netmiko_config']('show | json')
            .split('| json')[1]
            .split('[edit]')[0]
        ),
        comment='Device config',
    )
