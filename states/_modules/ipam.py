# -*- coding: utf-8 -*-

import logging, copy, ipaddress

__virtualname__ = "ipam"

log = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__

def comment():
    """
    Shortcut for ipam.report(report = False)

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if IP addresses returned; false otherwise

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy ipam.comment
    """
    return report(report = False, comment = True)


def report(report = True, comment = True):
    """
    Show salt managed IP addresses assigned to this router.

    A sorted list of the router's salt managed IP addresses is also displayed in
    the comment.

    :param report: Suppresses serialized dictionary out put if False.
    :param comment: Suppresses sorted list output to comment put if False.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if IP addresses returned; false otherwise

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy ipam.report
        salt sin1-proxy ipam.report comment=False

    """

    router   = __grains__['id']

    loopback = __pillar__['znsl_loopback']
    ifaces   = __pillar__['znsl_ethernet']
    tunnels  = __pillar__['znsl_tunnels']

    data = {}
    report_data = {}
    ret = {}

    report_text = "Salt managed addresses on this device:\n----------\n"

    if router in loopback:
        data.update(loopback[router])
    if router in ifaces:
        data.update(ifaces[router])
    if router in tunnels:
        data.update(tunnels[router])

    for iface, iface_data in data.items():
        if 'address' in iface_data:
            for addr, addr_data in iface_data['address'].items():

                cidr = addr.split('/')

                report_data[cidr[0]] = {}
                report_data[cidr[0]]['cidr'] = cidr[1]
                report_data[cidr[0]]['device'] = router
                report_data[cidr[0]]['interface'] = iface

                if 'description' in iface_data:
                    report_data[cidr[0]]['description'] = iface_data['description']

                if 'meta' in addr_data:
                    report_data[cidr[0]]['meta'] = copy.deepcopy(addr_data['meta'])

    if report:
        ret.update({'out': report_data, 'result': True})

    if comment:
        iplist = list(report_data.keys())
        ip4list = []
        ip6list = []

        for ip in iplist:
            try:
                ipaddress.IPv6Address(ip)
                ip6list.append(ip)
            except ipaddress.AddressValueError:
                ip4list.append(ip)

        sort4 = sorted(ip4list, key = ipaddress.IPv4Address)
        sort6 = sorted(ip6list, key = ipaddress.IPv6Address)
        iplist = sort6 + sort4

        for ip in iplist:
            description = ""
            if 'description' in report_data[ip]:
                description = report_data[ip]['description']

            report_text += "{0:30} {1:10} {2:40}\n".format(ip + '/' + report_data[ip]['cidr'], 
                    report_data[ip]['interface'], description)

        ret.update({'comment': report_text})

    ret.update({'result': True})

    return ret
