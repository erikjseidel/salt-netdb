import logging

__virtualname__ = "isis"

logger = logging.getLogger(__file__)

_COLUMN = 'protocol'

#  IS-IS disabled interfaces stored in this redis key.
_REDIS_KEY = 'isis_disabled'


def __virtual__():
    return __virtualname__


def _get_config():
    column = __utils__['column.pull'](_COLUMN).get('out')
    if not column:
        return {'result': False, 'comment': 'no IGP config found for this router'}

    isis = column.get('isis')
    if not isis:
        return {'result': False, 'comment': 'no IGP config found for this router'}

    return {'result': True, 'out': isis}


def _is_marked_disabled(interface):
    """
    Checks if an IS-IS interface is disabled. Wrapper around generic net_redis entry functions.
    """
    return __salt__['net_redis.check_entry'](_REDIS_KEY, interface)


def _remove_disable_mark(interface):
    """
    Removes an IS-IS interface disabled list. Wrapper around generic net_redis entry functions.
    """

    if not interface:
        return {"result": False, "comment": "No IS-IS interface selected."}

    return __salt__['net_redis.remove_entry'](_REDIS_KEY, interface)


def _mark_disabled_iface(interface):
    """
    Adds an IS-IS interface disabled list. Wrapper around generic net_redis entry functions.
    """

    if not interface:
        return {"result": False, "comment": "No IS-IS interface selected."}

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

        salt sin2 isis.generate

    """
    config = _get_config()
    if not config.get('result'):
        return config

    isis = config.get('out')

    new_ints = []

    for interface in isis['interfaces']:
        if not _is_marked_disabled(interface['name'])['out']:
            new_ints.append(interface)

    isis['interfaces'] = new_ints

    config.update(
        {
            'out': isis,
            'comment': 'IS-IS configuration generated for ' + __grains__['id'],
        }
    )

    return config


def enable_interface(interface, test=False, debug=False, force=False):
    """
    Enable IS-IS on a salt managed IS-IS interface. The interface must exist in netdb.

    :param interface: The name of the interface to be enabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for an interface not marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface is successfully enabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin2 isis.enable_interface tun261
        salt sin2 isis.enable_interface tun261 test=True
        salt sin2 isis.enable_interface tun261 force=False

    """
    name = 'isis_enable_interface'

    ret = {}

    if not isinstance(force, bool):
        return {"result": False, "comment": "force option only accepts true or false."}

    if not interface:
        return {"result": False, "comment": "No interface selected."}

    igp = _get_config()
    if not igp.get('result'):
        return igp

    isis = igp['out']

    iface = next(
        (item for item in isis['interfaces'] if item['name'] == interface), None
    )

    if not iface:
        ret = {"result": False, "comment": "IS-IS interface not found."}
    else:
        ret = _is_marked_disabled(interface)

        if not ret['out'] and not force:
            ret = {
                "result": False,
                "comment": "IS-IS interface not marked as disabled in REDIS. Use force=true to commit anyway.",
            }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="set protocols isis interface {{ interface }}",
                    test=test,
                    debug=debug,
                    commit_comment="enable IS-IS on interface " + interface,
                    interface=interface,
                )
            )
            # force means it didn't have the mark anyway.
            if not force and not test:
                _remove_disable_mark(interface)

    return ret


def disable_interface(interface, test=False, debug=False, force=False):
    """
    Disable IS-IS on a salt managed IS-IS interface. The interface must exist in netdb.
    Passive (i.e. loopback / dummy) interfaces cannot be disabled.

    :param interface: The name of the interface to be disabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for an interface marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface is successfully disabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin2 isis.disable_interface tun261
        salt sin2 isis.disable_interface tun261 test=True
        salt sin2 isis.disable_interface tun261 force=False

    """
    name = 'isis_disable_interface'

    ret = {}

    if not isinstance(force, bool):
        return {"result": False, "comment": "force option only accepts true or false."}

    if not interface:
        return {"result": False, "comment": "No interface selected."}

    igp = _get_config()
    if not igp.get('result'):
        return igp

    isis = igp['out']

    iface = next(
        (item for item in isis['interfaces'] if item['name'] == interface), None
    )

    if not iface:
        ret = {"result": False, "comment": "IS-IS interface not found."}
    elif 'passive' in iface.keys() and iface['passive']:
        ret = {
            "result": False,
            "comment": "IS-IS passive interface cannot be disabled.",
        }
    else:
        ret = _is_marked_disabled(interface)

        if ret['out'] and not force:
            ret = {
                "result": False,
                "comment": "IS-IS interface already marked as disabled in REDIS. Use force=true to commit anyway.",
            }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="delete protocols isis interface {{ interface }}",
                    test=test,
                    debug=debug,
                    commit_comment="disable IS-IS on interface " + interface,
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

        salt sin2 isis.overload enable=True
        salt sin2 isis.overload enable=False test=True
        salt sin2 isis.overload True debug=True

    """

    name = 'isis_overload'

    if not isinstance(enable, bool):
        return {"result": False, "comment": "Only accepts true or false."}

    template = "delete protocols isis set-overload-bit"
    comment = "IS-IS overload bit removed"

    if enable:
        template = "set protocols isis set-overload-bit"
        comment = "IS-IS overload bit set"

    return __salt__['net.load_template'](
        template_name=name,
        template_source=template,
        test=test,
        debug=debug,
        commit_comment=comment,
    )


def adj():
    """
    Show the router's IS-IS adjacencies (i.e. neighbours). This call is a wrapper around net.cli.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if adjacency information returned; false otherwise
       * comment: (str) A list of salt managed IS-IS interfaces

    CLI Example::

    .. code-block:: bash

        salt sin2 isis.adj

    """

    config = _get_config()

    ret = __salt__['net.cli']("show isis neighbor")

    disabled_interfaces = _get_disabled_ifaces().get('out')

    isis = config.get('out')
    if isis:
        iface_list = []
        for iface in isis['interfaces']:
            data = iface['name']
            if 'passive' in iface.keys() and iface['passive']:
                data += "\t[passive]"
            if iface['name'] in disabled_interfaces:
                data += "\t[disabled]"
            iface_list.append(data)

        ret['comment'] = "salt managed IS-IS interfaces:\n--- \n" + '\n'.join(
            iface_list
        )
    else:
        if config.get('error'):
            ret['comment'] = "netdb API down"
        else:
            ret['comment'] = "salt / netdb managed ISIS not present on this router"

    return ret


def sum():
    """
    Show a summary of the router's IS-IS state. This call is a wrapper around net.cli.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if summary returned; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin2 isis.sum

    """
    return __salt__['net.cli']("show isis summary")


def interface():
    """
    Show the router's IS-IS iterfaces. This call is a wrapper around net.cli.

    A list of the router's salt managed IS-IS interfaces is also displayed in the comment.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface information returned; false otherwise
       * comment: (str) A list of salt managed IS-IS interfaces

    CLI Example::

    .. code-block:: bash

        salt sin2 isis.interface

    """

    config = _get_config()

    ret = __salt__['net.cli']("show isis interface")

    disabled_interfaces = _get_disabled_ifaces().get('out')

    isis = config.get('out')
    if isis:
        iface_list = []
        for iface in isis['interfaces']:
            data = iface['name']
            if 'passive' in iface.keys() and iface['passive']:
                data += "\t[passive]"
            if iface['name'] in disabled_interfaces:
                data += "\t[disabled]"
            iface_list.append(data)

        ret['comment'] = "salt managed IS-IS interfaces:\n--- \n" + '\n'.join(
            iface_list
        )
    else:
        if config.get('error'):
            ret['comment'] = "netdb API down"
        else:
            ret['comment'] = "salt / netdb managed ISIS not present on this router"

    return ret
