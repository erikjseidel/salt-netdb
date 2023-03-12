# -*- coding: utf-8 -*-

import logging
import copy

__virtualname__ = "loopback"

log = logging.getLogger(__file__)

_PILLAR = 'znsl_loopback'


def __virtual__():
    if ( _PILLAR in __pillar__.keys() ):
        if __grains__['id'] in __pillar__[_PILLAR].keys():
            return __virtualname__
    else:
        return ( False, 'No salt managed loopback interfaces found on this router. Module not loaded.' )


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
    router = __grains__['id']
    ifaces = __pillar__[_PILLAR][router]
    
    ret_ifaces = copy.deepcopy(ifaces)

    ret = {'out': {}, 'result': False, 'error': False}

    if not (ret_ifaces):
        ret.update(
            {
                'comment': 'Failed to fetch loopback data',
                'error': True,
            }
        )
        return ret

    ret.update({'result': True, 'out': ret_ifaces})

    return ret


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

    router = __grains__['id']
    ifaces = __pillar__[_PILLAR][router].keys()

    ret = {"result": False, "comment": "unsupported operating system."}


    if (
        __grains__['os'] == "vyos"
       ):

        ret.update(
            __salt__['net.cli'](
                "show interface dummy",
            )
        )
    
    iface_list = []
    for interface in ifaces:
        data = interface
        iface_list.append(data)

    ret['comment'] = "salt managed loopback (dummy) interfaces:\n--- \n" + '\n'.join( iface_list )

    return ret
