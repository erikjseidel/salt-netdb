# -*- coding: utf-8 -*-

import logging, copy, json
import socket, struct
import salt.utils.http

__virtualname__ = "tunnel"

log = logging.getLogger(__file__)

_COLUMN = 'interface'

# Disabled tunnels stored in this redis key.
_REDIS_KEY = 'tunnel_disabled'

def __virtual__():
    return __virtualname__


def _netdb_pull():
    router = __grains__['id']
    netdb_answer =  __salt__['netdb.get_column'](_COLUMN)

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        return netdb_answer
    
    interfaces = netdb_answer['out']

    tunnels = {}

    for iface, iface_data in interfaces[router]['interfaces'].items():
        if iface.startswith('tun'):
            tunnels[iface] = iface_data

    return { 'result': True, 'out': tunnels }


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

        salt sin1-proxy tunnel.generate

    """

    ret_tunnels = _netdb_pull()
    if not ret_tunnels['result']:
        ret_tunnels.update({ 'error': True })
        return ret_tunnels

    tunnels = ret_tunnels['out']

    ret = {'out': {}, 'result': False, 'error': False}

    disabled_tunnels = _get_disabled_tunnels()['out']

    for tunnel, settings in tunnels.items():
        # netdb overrides redis if setting present there.
        if 'disabled' not in settings:
            if tunnel in disabled_tunnels:
                settings['disabled'] = True
            else:
                settings['disabled'] = False

        if 'key' in settings:
            settings['key_vyos'] = _ip2long(settings['key'])

    ret.update({'result': True, 'out': tunnels})

    return ret


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

        salt sin1-proxy tunnel.enable tun261
        salt sin1-proxy tunnel.enable tun261 test=True
        salt sin1-proxy tunnel.enable tun261 force=False

    """

    name = 'enable_tunnel'
    ret = {"result": False, "comment": "Tunnel does not exist on selected router."}

    if not tunnel:
        ret = {"result": False, "comment": "No tunnel selected."}

    ret_tunnels = _netdb_pull()
    if not ret_tunnels['result']:
        return ret_tunnels

    tunnels = ret_tunnels['out'].keys()

    if tunnel not in tunnels:
        ret = {"result": False, "comment": "Tunnel not found on this router."}
    else:
        ret = _is_marked_disabled(tunnel)

        if not ret['out'] and not force:
            ret = {
                "result": False,
                "comment": "Tunnel not marked as disabled in REDIS. Use force=true to commit anyway."
                }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="delete interface tunnel {{ tunnel }} disable",
                    test=test,
                    debug=debug,
                    commit_comment = "enable tunnel " + tunnel,
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

        salt sin1-proxy tunnel.disable tun261
        salt sin1-proxy tunnel.disable tun261 test=True
        salt sin1-proxy tunnel.disable tun261 force=False

    """

    name = 'disable_tunnel'
    ret = {"result": False, "comment": "Tunnel does not exist on selected router."}

    if not tunnel:
        ret = {"result": False, "comment": "No tunnel selected."}

    ret_tunnels = _netdb_pull()
    if not ret_tunnels['result']:
        return ret_tunnels

    tunnels = ret_tunnels['out'].keys()

    if tunnel not in tunnels:
        ret = {"result": False, "comment": "Tunnel not found on this router."}
    else:
        ret = _is_marked_disabled(tunnel)

        if ret['out'] and not force:
            ret = {
                "result": False,
                "comment": "Tunnel is already marked disabled in REDIS. Use force=true to commit anyway."
                }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="set interface tunnel {{ tunnel }} disable",
                    test=test,
                    debug=debug,
                    commit_comment = "disable tunnel " + tunnel,
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

        salt sin1-proxy tunnel.display

    """

    ret_tunnels = _netdb_pull()

    ret = {"result": False, "comment": "unsupported operating system."}

    if (
        __grains__['os'] == "vyos"
       ):

        ret.update(
            __salt__['net.cli'](
                "show interface tunnel",
            )
        )
    
    disabled_tunnels = _get_disabled_tunnels()['out']

    if ret_tunnels['result']:
        tunnel_list = []
        tunnels = ret_tunnels['out']
        for tunnel in tunnels:
            data = tunnel
            if tunnel in disabled_tunnels:
                data += "\t[disabled]"
            tunnel_list.append(data)

        ret['comment'] = "salt managed tunnels:\n--- \n" + '\n'.join( tunnel_list )
    else:
        ret['comment'] = "netdb API down"

    return ret
