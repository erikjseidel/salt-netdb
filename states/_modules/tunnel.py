import logging, socket, struct

__virtualname__ = "tunnel"

logger = logging.getLogger(__file__)

_COLUMN = 'interface'

# Disabled tunnels stored in this redis key.
_REDIS_KEY = 'tunnel_disabled'


def __virtual__():
    return __virtualname__


def _get_tunnels():
    interfaces = __utils__['column.pull'](_COLUMN).get('out')
    if not interfaces:
        return {'result': False}

    tunnels = {}

    for iface, iface_data in interfaces.items():
        if iface.startswith('tun'):
            tunnels[iface] = iface_data

    return {'result': True, 'out': tunnels}


def _ip2long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]


def _is_marked_disabled(tunnel):
    """
    Checks if a tunnel is disabled. Wrapper around generic net_redis entry functions.
    """
    return __salt__['net_redis.check_entry'](_REDIS_KEY, tunnel)


def _remove_disable_mark(tunnel, tunnels):
    """
    Removes a tunnel from the disabled list. Wrapper around generic net_redis entry functions.
    """

    if not tunnel:
        return {"result": False, "comment": "No tunnel selected."}

    if tunnel not in tunnels:
        return {"result": False, "comment": "Tunnel not found."}

    return __salt__['net_redis.remove_entry'](_REDIS_KEY, tunnel)


def _mark_disabled_tunnel(tunnel, tunnels):
    """
    Adds a tunnel to disabled list. Wrapper around generic net_redis entry functions.
    """

    if not tunnel:
        return {"result": False, "comment": "No tunnel selected."}

    if tunnel not in tunnels:
        return {"result": False, "comment": "Tunnel not found."}

    return __salt__['net_redis.add_entry'](_REDIS_KEY, tunnel)


def _get_disabled_tunnels():
    """
    Retrieves list of disabled tunnels. Wrapper around generic net_redis entry functions.
    """
    return __salt__['net_redis.get_entries'](_REDIS_KEY)


def generate():
    """
    Generate dictionary for "state.apply tunnels". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1 tunnel.generate

    """
    ret_tunnels = _get_tunnels()
    if not ret_tunnels['result']:
        return ret_tunnels

    tunnels = ret_tunnels.get('out')

    disabled_tunnels = _get_disabled_tunnels().get('out')

    for tunnel, settings in tunnels.items():
        # netdb overrides redis if setting present there.
        if 'disabled' not in settings:
            if tunnel in disabled_tunnels:
                settings['disabled'] = True
            else:
                settings['disabled'] = False

        if 'key' in settings:
            settings['key_vyos'] = _ip2long(settings['key'])

    return {
        'result': True,
        'out': tunnels,
        'comment': 'Tunnel interfaces generated for ' + __grains__['id'],
    }


def enable(tunnel, test=False, debug=False, force=False):
    """
    Enable a salt managed tunnel. The router and tunnel must exist in netdb.

    :param tunnel: The name of the tunnel to be enabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for a tunnel not marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if tunnel is successfully enabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1 tunnel.enable tun261
        salt sin1 tunnel.enable tun261 test=True
        salt sin1 tunnel.enable tun261 force=False

    """
    name = 'enable_tunnel'
    ret = {"result": False}

    if not tunnel:
        ret = {"result": False, "comment": "No tunnel selected."}

    ret_tunnels = _get_tunnels()
    if not ret_tunnels['result']:
        return ret_tunnels

    tunnels = ret_tunnels['out'].keys()

    if tunnel not in tunnels:
        ret = {"result": False, "comment": "Tunnel not found on this router."}
    else:
        ret = _is_marked_disabled(tunnel)

        if not ret.get('out') and not force:
            ret = {
                "result": False,
                "comment": "Tunnel not marked as disabled in REDIS. Use force=true to commit anyway.",
            }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="delete interface tunnel {{ tunnel }} disable",
                    test=test,
                    debug=debug,
                    commit_comment="enable tunnel " + tunnel,
                    tunnel=tunnel,
                )
            )
            # force means it didn't have the mark anyway.
            if not force and not test:
                _remove_disable_mark(tunnel, tunnels)

    return ret


def disable(tunnel, test=False, debug=False, force=False):
    """
    Disable a salt managed tunnel. The router and tunnel must exist in netdb.

    :param tunnel: The name of the tunnel to be disabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for a tunnel marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if tunnel is successfully disabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1 tunnel.disable tun261
        salt sin1 tunnel.disable tun261 test=True
        salt sin1 tunnel.disable tun261 force=False

    """
    name = 'disable_tunnel'
    ret = {"result": False}

    if not tunnel:
        ret = {"result": False, "comment": "No tunnel selected."}

    ret_tunnels = _get_tunnels()
    if not ret_tunnels['result']:
        return ret_tunnels

    tunnels = ret_tunnels['out'].keys()

    if tunnel not in tunnels:
        ret = {"result": False, "comment": "Tunnel not found on this router."}
    else:
        ret = _is_marked_disabled(tunnel)

        if ret.get('out') and not force:
            ret = {
                "result": False,
                "comment": "Tunnel is already marked disabled in REDIS. Use force=true to commit anyway.",
            }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="set interface tunnel {{ tunnel }} disable",
                    test=test,
                    debug=debug,
                    commit_comment="disable tunnel " + tunnel,
                    tunnel=tunnel,
                )
            )
            # force means it didn't have the mark anyway.
            if not force and not test:
                _mark_disabled_tunnel(tunnel, tunnels)

    return ret


def display():
    """
    Show the router's tunnels. This call is a wrapper around net.cli.

    A list of the router's salt managed tunnels is also displayed in the comment.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface information returned; false otherwise
       * comment: (str) A list of salt managed tunnels

    CLI Example::

    .. code-block:: bash

        salt sin1 tunnel.display

    """
    ret_tunnels = _get_tunnels()

    ret = __salt__['net.cli']("show interface tunnel")

    disabled_tunnels = _get_disabled_tunnels().get('out')

    if ret_tunnels.get('result'):
        tunnel_list = []
        tunnels = ret_tunnels['out']
        for tunnel in tunnels:
            data = tunnel
            if tunnel in disabled_tunnels:
                data += "\t[disabled]"
            tunnel_list.append(data)

        ret['comment'] = "salt managed tunnels:\n--- \n" + '\n'.join(tunnel_list)
    else:
        ret['comment'] = "netdb API down"

    return ret
