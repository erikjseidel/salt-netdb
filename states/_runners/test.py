
import logging, copy
from netaddr   import IPSet
from ipaddress import ip_interface, ip_network
from copy      import deepcopy

__virtualname__ = "test"


def __virtual__():
    return __virtualname__


def column_item(minion, *args, **kwargs):

    ret = __salt__['salt.execute'](minion, 'column.item', args, kwarg=kwargs)

    return ret.get(minion) or ret
