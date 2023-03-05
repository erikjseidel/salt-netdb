# -*- coding: utf-8 -*-

import logging
import copy

__virtualname__ = "isis"

log = logging.getLogger(__file__)

_PILLAR = 'znsl_isis'
#  IS-IS disabled interfaces stored in this redis key.
_REDIS_KEY = 'isis_disabled'


def __virtual__():
    if ( _PILLAR in __pillar__.keys() ):
        return __virtualname__
    else:
        return ( False, 'IS-IS not enabled or not salt managed on this router. Module not loaded.' )


def _is_marked_disabled(interface):
    """
    Checks if an IS-IS interface is disabled. Wrapper around generic net_redis entry functions. 
    """
    isis_interfaces = __pillar__[_PILLAR]['interfaces']

    return __salt__['net_redis.check_entry'](_REDIS_KEY, interface)


def _remove_disable_mark(interface):
    """
    Removes an IS-IS interface disabled list. Wrapper around generic net_redis entry functions.
    """
    router = __grains__['id']
    isis_interfaces = __pillar__[_PILLAR]['interfaces']

    if not interface:
        return {"result": False, "comment": "No IS-IS interface selected."}

    if not next((item for item in isis_interfaces if item['name'] == interface), None):
        return {"result": False, "comment": "IS-IS interface not found."}

    return __salt__['net_redis.remove_entry'](_REDIS_KEY, interface)


def _mark_disabled_iface(interface):
    """
    Adds an IS-IS interface disabled list. Wrapper around generic net_redis entry functions.
    """
    router = __grains__['id']
    isis_interfaces = __pillar__[_PILLAR]['interfaces']

    if not interface:
        return {"result": False, "comment": "No IS-IS interface selected."}

    if not next((item for item in isis_interfaces if item['name'] == interface), None):
        return {"result": False, "comment": "IS-IS interface not found."}

    return __salt__['net_redis.add_entry'](_REDIS_KEY, interface)


def _get_disabled_ifaces():
    """
    Retrieves list of IS-IS disabled interfaces. Wrapper around generic net_redis entry functions.
    """
    return __salt__['net_redis.get_entries'](_REDIS_KEY)


def generate():
    """
    Generate dictionary for "state.apply isis". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy isis.generate

    """

    isis = __pillar__[_PILLAR]

    ret_isis = copy.deepcopy(isis)
    ret = {'out': {}, 'result': False, 'error': False}

    if not (ret_isis):
        ret.update(
            {
                'comment': 'IS-IS data not found',
                'error': True,
            }
        )
        return ret

    new_ints = []

    for interface in ret_isis['interfaces']:
       if not _is_marked_disabled(interface['name'])['out']:
            new_ints.append(interface)

    ret_isis['interfaces'] = new_ints

    ret.update({'result': True, 'out': ret_isis })

    return ret


def enable_interface(interface, test=False, debug=False, force=False):
    """
    Enable IS-IS on a salt managed IS-IS interface. The interface must exist in the router's
    IS-IS pillar.

    :param interface: The name of the interface to be enabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for an interface not marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface is successfully enabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy isis.enable_interface tun261 
        salt sin1-proxy isis.enable_interface tun261 test=True
        salt sin1-proxy isis.enable_interface tun261 force=False

    """

    isis = __pillar__[_PILLAR]

    name = 'isis_enable_interface'

    ret = {}

    if not isinstance(force, bool):
        return {"result": False, "comment": "force option only accepts true or false."}

    if not interface:
        return {"result": False, "comment": "No interface selected."}

    iface = next((item for item in isis['interfaces'] if item['name'] == interface), None)

    if not iface:
        ret = {"result": False, "comment": "IS-IS interface not found."}
    else:
        ret = _is_marked_disabled(interface)

        if not ret['out'] and not force:
            ret = { 
                "result": False, 
                "comment": "IS-IS interface not marked as disabled in REDIS. Use force=true to commit anyway." 
                }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="set protocols isis interface {{ interface }}",
                    test=test,
                    debug=debug,
                    commit_comment = "enable IS-IS on interface " + interface,
                    interface=interface,
                )
            )
            # force means it didn't have the mark anyway.
            if not force and not test:
                _remove_disable_mark(interface)

    return ret


def disable_interface(interface, test=False, debug=False, force=False):
    """
    Disable IS-IS on a salt managed IS-IS interface. The interface must exist in the router's
    IS-IS pillar. Passive (i.e. loopback / dummy) interfaces cannot be disabled.

    :param interface: The name of the interface to be disabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for an interface marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface is successfully disabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy isis.disable_interface tun261 
        salt sin1-proxy isis.disable_interface tun261 test=True
        salt sin1-proxy isis.disable_interface tun261 force=False

    """

    isis = __pillar__[_PILLAR]

    name = 'isis_disable_interface'

    ret = {}

    if not isinstance(force, bool):
        return {"result": False, "comment": "force option only accepts true or false."}

    if not interface:
        return {"result": False, "comment": "No interface selected."}

    iface = next((item for item in isis['interfaces'] if item['name'] == interface), None)

    if not iface:
        ret = {"result": False, "comment": "IS-IS interface not found."}
    elif 'passive' in iface.keys() and iface['passive']:
        ret = {"result": False, "comment": "IS-IS passive interface cannot be disabled."}
    else:
        ret = _is_marked_disabled(interface)

        if ret['out'] and not force:
            ret = { 
                "result": False, 
                "comment": "IS-IS interface already marked as disabled in REDIS. Use force=true to commit anyway." 
                }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="delete protocols isis interface {{ interface }}",
                    test=test,
                    debug=debug,
                    commit_comment = "disable IS-IS on interface " + interface,
                    interface=interface,
                )
            )
            # force means its already marked.
            if not force and not test:
                _mark_disabled_iface(interface)

    return ret


def overload(enable, test=False, debug=False):
    """
    Set / unset the IS-IS overload bit on the router.

    :param enable: True to enable overload bit. False to disable overload bit.
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if overload bit successfully enabled / disabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy isis.overload enable=True
        salt sin1-proxy isis.overload enable=False test=True
        salt sin1-proxy isis.overload True debug=True

    """

    name = 'isis_overload'

    if not isinstance(enable, bool):
        return {"result": False, "comment": "Only accepts true or false."}

    template = "delete protocols isis set-overload-bit"
    comment  = "IS-IS overload bit removed"

    if ( enable ):
        template = "set protocols isis set-overload-bit"
        comment  = "IS-IS overload bit set"

    return (
        __salt__['net.load_template'](
            template_name=name,
            template_source=template,
            test=test,
            debug=debug,
            commit_comment = comment,
        )
    )


def adj():
    """
    Show the router's IS-IS adjacencies (i.e. neighbours). This call is a wrapper around net.cli.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if adjacency information returned; false otherwise
       * comment: (str) A list of salt managed IS-IS interfaces

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy isis.adj

    """

    isis = __pillar__[_PILLAR]

    ret = {"result": False, "comment": "unsupported operating system."}

    if ( __grains__['os'] == "vyos" ):
        ret.update(
            __salt__['net.cli'](
                "show isis neighbor",
            )
        )

    disabled_interfaces = _get_disabled_ifaces()['out']

    iface_list = []
    for iface in isis['interfaces']:
        data = iface['name']
        if 'passive' in iface.keys() and iface['passive']:
            data += "\t[passive]"
        if iface['name'] in disabled_interfaces:
            data += "\t[disabled]"
        iface_list.append(data)

    ret['comment'] = "salt managed IS-IS interfaces:\n--- \n" + '\n'.join( iface_list )

    return ret


def sum():
    """
    Show a summary of the router's IS-IS state. This call is a wrapper around net.cli.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if summary returned; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy isis.sum

    """

    ret = {"result": False, "comment": "unsupported operating system."}

    if ( __grains__['os'] == "vyos" ):
        ret.update(
            __salt__['net.cli'](
                "show isis summary",
            )
        )

    return ret


def interface():
    """
    Show the router's IS-IS iterfaces. This call is a wrapper around net.cli.

    A list of the router's salt managed IS-IS interfaces is also displayed in the comment.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface information returned; false otherwise
       * comment: (str) A list of salt managed IS-IS interfaces

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy isis.interface

    """

    isis = __pillar__[_PILLAR]

    ret = {"result": False, "comment": "unsupported operating system."}

    if ( __grains__['os'] == "vyos" ):
        ret.update(
            __salt__['net.cli'](
                "show isis interface",
            )
        )
    else:
        return ret

    disabled_interfaces = _get_disabled_ifaces()['out']

    iface_list = []
    for iface in isis['interfaces']:
        data = iface['name']
        if 'passive' in iface.keys() and iface['passive']:
            data += "\t[passive]"
        if iface['name'] in disabled_interfaces:
            data += "\t[disabled]"
        iface_list.append(data)

    ret['comment'] = "salt managed IS-IS interfaces:\n--- \n" + '\n'.join( iface_list  )

    return ret
