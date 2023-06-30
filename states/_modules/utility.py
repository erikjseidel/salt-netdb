import re, logging
from netaddr import IPAddress
from netaddr.core import AddrFormatError

__virtualname__ = "utility"

logger = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__


def ping_test(dst_ip, src_ip, count, threshold):
    """
    Run a ping flood test to validate interface connectivity.

    :param dst_ip: Destination IP address
    :param src_ip: Source IP address
    :param count: Number of packets to send (between 10 and 1000)
    :param threshold: Maximum loss threshold (float) for a pass=True result
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface information returned; false otherwise
       * out: Test result and details

    CLI Example::

    .. code-block:: bash

        salt sin2 utility.ping_test 23.181.64.98 23.181.64.97 1000 0.5

    """
    name = 'ping_test'

    okay = True
    result = { 'result' : False }

    if not ( isinstance(count, int) and count in range(10, 1001) ):
        okay = False
        result['comment'] = 'count must be between 10 and 1000'

    if not isinstance(threshold, float):
        okay = False
        result['comment'] = 'threshold must be a valid floating point number'

    try:
        if IPAddress(src_ip).version != IPAddress(dst_ip).version:
            okay = False
            result['comment'] = 'src_ip and dst_ip family mismatch'

    except AddrFormatError:
        okay = False
        result['comment'] = 'invalid IP address input'

    if not okay:
        return result

    command = f'ping {dst_ip} source {src_ip} count {count} flood'

    ret = __salt__['net.cli'](command)
    if not ret['result']:
        return ret

    p = re.search(r'(\d*[\.|\,]?\d+)%', ret['out'][command])
    if p:
        loss = p.group()
    else:
        return {
                'result'  : False,
                'out'     : ret['out'],
                'comment' : ' Invalid ping result',
                }

    success = False
    if float(loss[:-1]) < threshold:
        success = True

    out = {
            'output' : ret['out'],
            'loss'   : loss,
            'pass'   : success,
            }

    return {
            'result'  : True,
            'out'     : out,
            'comment' : 'Ping test results'
            }
