import re, logging, json
from netaddr import IPAddress
from netaddr.core import AddrFormatError

__virtualname__ = "utility"

logger = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__


def bgp_session_check(neighbor_ip):
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
    name = 'bg_session_check'

    okay = True
    result = { 'result' : False }

    try:
        family = 'ipv6' if IPAddress(neighbor_ip).version == 6 else 'ip'

    except AddrFormatError:
        okay = False
        result['comment'] = 'invalid IP address input'

    if not okay:
        return result

    command = f'show {family} bgp neighbor {neighbor_ip} | match "BGP state"'

    ret = __salt__['net.cli'](command)
    if not ret['result']:
        return ret

    p = ret['out'][command]
    if p:
        state = p.split(',')[0].split(' = ')[1].upper()
    else:
        return {
                'result'  : False,
                'out'     : ret['out'],
                'comment' : 'BGP session not found',
                }

    out = {
            'output'      : ret['out'],
            'state'       : state,
            'established' : (state == 'ESTABLISHED'),
            }

    return {
            'result'  : True,
            'out'     : out,
            'comment' : 'BGP session check results'
            }


def get_config():
    """
    """

    resp = __salt__['napalm.netmiko_config']('show | json')

    json_string = resp.split('| json')[1].split('[edit]')[0]

    return {
            'result' : True,
            'out'    : json.loads(json_string),
            'comment' : 'Device config',
            }
