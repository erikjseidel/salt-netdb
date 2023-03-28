# -*- coding: utf-8 -*-

import logging, copy, json

__virtualname__ = "interface"

log = logging.getLogger(__file__)

_COLUMN = 'interface'

def __virtual__():
    return __virtualname__


def get(device = None, interface = None):
    """

    """

    filt = [ device, None, None, interface ]

    netdb_answer = __utils__['netdb_runner.request'](_COLUMN, data = filt, method='GET')

    return netdb_answer

    if not netdb_answer['result'] or not netdb_answer['out']:
        return netdb_answer

    data = {}



    ret.update({'result': True})

    return ret

