# -*- coding: utf-8 -*-

import logging, copy
from netaddr   import IPSet
from ipaddress import ip_interface, ip_network

__virtualname__ = "ipam"

log = logging.getLogger(__file__)

_COLUMN = 'interface'

_WARNING = """This utility returns only ip space that is managed by salt-netdb. In order for
it to return accurate free space, the entiret of the queried prefix must be
managed by salt-netdb. 
"""

def __virtual__():
    return __virtualname__


def report(device = None, out = True, comment = True):
    """
    Show salt managed IP addresses assigned to this router.

    A sorted list of the router's salt managed IP addresses is also displayed in
    the comment.

    :param device: Limit report to only the specified device.
    :param out: Suppresses serialized dictionary out put if False.
    :param comment: Suppresses sorted list output to comment put if False.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if IP addresses returned; false otherwise

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy ipam.report
        salt sin1-proxy ipam.report comment=False

    """

    if not isinstance(out, bool) or not isinstance(comment, bool):
        return {"result": False, "comment": "comment and out only accept true or false."}

    netdb_answer = __utils__['netdb_runner.request'](_COLUMN, method='GET')

    if not netdb_answer['result'] or not netdb_answer['out']:
        return netdb_answer

    data = {}

    # Not optimal. TBD: filter netdb query to just desired device in this case.
    if device:
        device = device.upper()
        if device in netdb_answer['out']:
            data[device] = netdb_answer['out'][device]
        else:
            return { 'result': False, 'comment': '%s: device not found' % device }
    else:
        data = netdb_answer['out']

    report_data = {}
    ret = {}

    report_text = "Salt managed addresses:\n----------\n"

    for device, interfaces in data.items():
        for iface, iface_data in interfaces['interfaces'].items():
            if 'address' in iface_data:
                for addr, addr_data in iface_data['address'].items():
 
                    cidr = addr.split('/')
 
                    report_data[cidr[0]] = {}
                    report_data[cidr[0]]['cidr'] = cidr[1]
                    report_data[cidr[0]]['device'] = device
                    report_data[cidr[0]]['interface'] = iface

                    if 'description' in iface_data:
                        report_data[cidr[0]]['description'] = iface_data['description']

                    if 'meta' in addr_data:
                        report_data[cidr[0]]['meta'] = copy.deepcopy(addr_data['meta'])

        if out:
            ret.update({'out': report_data, 'result': True})

        if comment:
            iplist = list(report_data.keys())

            for ip in iplist:
                description = ""
                if 'description' in report_data[ip]:
                    description = report_data[ip]['description']

                report_text += "{0:30} {1:10} {2:10} {3:40}\n".format(ip + '/' + report_data[ip]['cidr'], device,
                        report_data[ip]['interface'], description)

            ret.update({'comment': report_text})

    ret.update({'result': True})

    return ret


def chooser(prefix, out=True, comment=True):
    """
    Show available prefixes / free IP space within a given (super)prefix.

    In order for this function to by accurate, all IP a space within the
    the queried prefix must be managed by netdb - salt.

    :param prefix: The prefix whose free space is to be returned.
    :param out: Suppresses serialized dictionary out put if False.
    :param comment: Suppresses sorted list output to comment put if False.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if IP addresses returned; false otherwise
       * out: a list of free space in prefix and range formats

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy ipam.chooser prefix='23.181.64.0/24'

    """
    if not isinstance(out, bool) or not isinstance(comment, bool):
        return {"result": False, "comment": "comment and out only accept true or false."}

    try:
        network = ip_network(prefix)
    except:
        return { 'result': False, 'error': True, 'comment': 'Invalid prefix' }

    netdb_answer = __utils__['netdb_runner.request'](_COLUMN, method='GET')

    if not netdb_answer['result'] or not netdb_answer['out']:
        return netdb_answer

    data = netdb_answer['out']

    prefix_list  = []
    avail_addr = []

    for device, interfaces in data.items():
        for iface, iface_data in interfaces['interfaces'].items():
            if 'address' in iface_data:
                addresses = iface_data['address'].keys()
                for addr in addresses:
                    net = ip_interface(addr).network
                    try:
                        if net.subnet_of(network) and str(net) not in prefix_list:
                            prefix_list.append(str(net))
                    except:
                        continue

    available = IPSet( [str(network)] ) ^ IPSet(prefix_list)

    comment_text = "Available prefixes:\n-----\n"
    out_dict = {}
    for cidr in available.iter_cidrs():
        prefix = str(cidr)
        start  = str(cidr[0])
        end    = str(cidr[-1])

        out_dict[prefix] = {
                'start':  start,
                'end':    end,
                }

        comment_text += '%s [%s - %s]\n' % ( prefix, start, end )

    ret = { 'result': True, 'note': _WARNING }

    if out:
        ret.update({ 'out': out_dict })
    if comment:
        ret.update({ 'comment': comment_text })

    return ret
