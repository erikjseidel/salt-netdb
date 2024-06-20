import logging

__virtualname__ = "loopback"

logger = logging.getLogger(__file__)

_COLUMN = 'interface'


def __virtual__():
    return __virtualname__


def _get_loopbacks():
    interfaces = __utils__['column.pull'](_COLUMN).get('out')
    if not interfaces:
        return {'result': False}

    loopbacks = {}

    for iface, iface_data in interfaces.items():
        if iface.startswith('dum'):
            loopbacks[iface] = iface_data

    return {
        'result': True,
        'out': loopbacks,
        'comment': 'Loopback interfaces generated for ' + __grains__['id'],
    }


def generate():
    """
    Generate dictionary for "state.apply loopback". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1 loopback.generate

    """

    return _get_loopbacks()


def display():
    """
    Show the router's loopback (dummy) interfaces. This call is a wrapper around net.cli.

    A list of the router's salt managed loopback interfaces is also displayed in the comment.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface information returned; false otherwise
       * comment: (str) A list of salt managed loopback interfaces

    CLI Example::

    .. code-block:: bash

        salt sin1 loopback.display

    """
    ret_lo = _get_loopbacks()

    ret = __salt__['net.cli']("show interface dummy")

    if ret_lo['result']:
        ifaces = ret_lo.get('out')
        iface_list = []
        for interface in ifaces:
            data = interface
            iface_list.append(data)

        ret['comment'] = (
            "salt managed loopback (dummy) interfaces:\n--- \n" + '\n'.join(iface_list)
        )
    else:
        ret['comment'] = "netdb API down"

    return ret
