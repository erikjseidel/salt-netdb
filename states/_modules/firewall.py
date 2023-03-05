# -*- coding: utf-8 -*-

import logging
import copy

__virtualname__ = "firewall"

log = logging.getLogger(__file__)

_PILLAR = 'znsl_firewall'

def __virtual__():
    return __virtualname__


def generate():
    """
    Generate dictionary for "state.apply firewall". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy firewall.generate

    """

    firewall = __pillar__[_PILLAR]

    ret = {'out': {}, 'result': False, 'error': False}

    if not (firewall):
        ret.update(
            {
                'comment': 'Failed to get firewall data',
                'error': True,
            }
        )
        return ret
    
    router_roles = __grains__['roles']

    rules_out = {}

    router_roles.append('common')
    router_roles.append('custom_firewall')

    for role in router_roles:
        if role in firewall.keys():
            rules_out[role] = copy.deepcopy(firewall[role])

    ret.update({'result': True, 'out': rules_out})

    return ret
