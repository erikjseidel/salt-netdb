# -*- coding: utf-8 -*-

import logging
import copy

__virtualname__ = "loopback"

log = logging.getLogger(__file__)

_COLUMN = 'interface'

def __virtual__():
    return __virtualname__


def _netdb_pull():
    router = __grains__['id']
    netdb_answer =  __salt__['netdb.get_column'](_COLUMN)

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        return netdb_answer

    interfaces = netdb_answer['out']

    loopbacks = {}

    for iface, iface_data in interfaces[router].items():
        if iface.startswith('dum'):
            loopbacks[iface] = iface_data

    return { 'result': True, 'out': loopbacks }


def generate():
    """
    Generate dictionary for "state.apply loopback". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy loopback.generate

    """
    
    ret_lo = _netdb_pull()
    if not ret_lo['result']:
        return ret_lo

    ifaces = ret_lo['out']

    return {'result': True, 'out': ifaces}


def display():
    """
    Show the router's loopback (dummy) interfaces. This call is a wrapper around net.cli.

    A list of the router's salt managed loopback interfaces is also displayed in the comment.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface information returned; false otherwise
       * comment: (str) A list of salt managed loopback interfaces

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy loopback.display

    """

    ret_lo = _netdb_pull()

    ret = {"result": False, "comment": "unsupported operating system."}

    if (
        __grains__['os'] == "vyos"
       ):

        ret.update(
            __salt__['net.cli'](
                "show interface dummy",
            )
        )
    
    if ret_lo['result']:
        ifaces = ret_lo['out']
        iface_list = []
        for interface in ifaces:
            data = interface
            iface_list.append(data)

        ret['comment'] = "salt managed loopback (dummy) interfaces:\n--- \n" + '\n'.join( iface_list )
    else:
        ret['comment'] = "netdb API down"

    return ret
