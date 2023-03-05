# -*- coding: utf-8 -*-

import logging
import copy

__virtualname__ = "policy"

log = logging.getLogger(__file__)

_PILLAR = 'znsl_policy'

def __virtual__():
    return __virtualname__


def generate():
    """
    Generate dictionary for "state.apply policy". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy policy.generate

    """

    policy = __pillar__[_PILLAR]

    ret = {'out': {}, 'result': False, 'error': False}

    if not (policy):
        ret.update(
            {
                'comment': 'Failed to get policy data',
                'error': True,
            }
        )
        return ret
    
    router_roles = __grains__['roles']

    policy_out = {}

    router_roles.append('common')
    router_roles.append('custom_policy')

    for role in router_roles:
        if role in policy.keys():
            policy_out[role] = copy.deepcopy(policy[role])

    ret.update({'result': True, 'out': policy_out})

    return ret
