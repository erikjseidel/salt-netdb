import logging
import copy

__virtualname__ = "ethernet"

logger = logging.getLogger(__file__)

_COLUMN = 'interface'

# Disabled tunnels stored in this redis key.
_REDIS_KEY = 'ethernet_disabled'


def __virtual__():
    return __virtualname__


def _get_ethernet():
    interfaces = __utils__['column.pull'](_COLUMN).get('out')
    if not interfaces:
        return {'result': False}

    ethernet = {}

    for iface, iface_data in interfaces.items():
        if iface.startswith('eth') or iface.startswith('bond'):
            ethernet[iface] = iface_data

    return {'result': True, 'out': ethernet}


def _is_marked_disabled(interface):
    """
    Checks if an interface is disabled. Wrapper around generic net_redis entry functions.
    """
    return __salt__['net_redis.check_entry'](_REDIS_KEY, interface)


def _remove_disable_mark(interface):
    """
    Removes an interface from the disabled list. Wrapper around generic net_redis entry functions.
    """

    if not interface:
        return {"result": False, "comment": "No interface selected."}

    return __salt__['net_redis.remove_entry'](_REDIS_KEY, interface)


def _mark_disabled_interface(interface):
    """
    Adds an interface to disabled list. Wrapper around generic net_redis entry functions.
    """

    if not interface:
        return {"result": False, "comment": "No interface selected."}

    return __salt__['net_redis.add_entry'](_REDIS_KEY, interface)


def _get_disabled_interfaces():
    """
    Retrieves list of disabled tunnels. Wrapper around generic net_redis entry functions.
    """
    return __salt__['net_redis.get_entries'](_REDIS_KEY)


def generate():
    """
    Generate dictionary for "state.apply ethernet". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1 ethernet.generate

    """
    ret_ethernet = _get_ethernet()
    if not ret_ethernet.get('result'):
        return ret_ethernet

    ifaces = ret_ethernet.get('out')

    disabled_ifaces = _get_disabled_interfaces()['out']

    for interface, settings in ifaces.items():
        # netdb overrides redis if setting present there.
        if 'disabled' not in settings:
            if interface in disabled_ifaces:
                settings['disabled'] = True
            else:
                settings['disabled'] = False

        if settings['type'] == 'ethernet':
            settings['vyos_type'] = 'ethernet'
        elif settings['type'] == 'lacp':
            settings['vyos_type'] = 'bonding'
        elif settings['type'] == 'vlan':
            settings['vyos_type'] = 'vif'
            if 'bond' in settings['vlan']['parent']:
                settings['vlan']['parent_vyos_type'] = 'bonding'
            elif 'eth' in settings['vlan']['parent']:
                settings['vlan']['parent_vyos_type'] = 'ethernet'
            else:
                return {
                    'result': False,
                    'comment': interface + ": unsupported vlan parrent interface type!",
                }
        else:
            return {
                'result': False,
                'comment': interface + ": unsupported interface type!",
            }

    return {
        'result': True,
        'out': ifaces,
        'comment': 'Ethernet interfaces generated for ' + __grains__['id'],
    }


def enable(interface, test=False, debug=False, force=False):
    """
    Enable a salt managed ethernet, vlan or bundle interface. The interface must exist in
    netdb.

    :param interface: The name of the interface to be enabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for a tunnel not marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface is successfully enabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1 ethernet.enable bond0.17
        salt sin1 ethernet.enable bond0.15 test=True
        salt sin1 ethernet.enable eth1 force=False

    """
    name = 'enable_ethernet'
    ret = {"result": False, "comment": "Interface does not exist on selected router."}

    if not interface:
        ret = {"result": False, "comment": "No interface selected."}

    ret_ifaces = _get_ethernet()
    if not ret_ifaces.get('result'):
        return ret_ifaces

    ifaces = ret_ifaces.get('out')

    if interface not in ifaces.keys():
        ret = {"result": False, "comment": "Interface not found on this router."}
    else:
        iface_type = ifaces[interface]['type']
        statement = ''

        if iface_type == 'vlan':
            vlan_id = ifaces[interface]['vlan']['id']
            parent = ifaces[interface]['vlan']['parent']

            parent_type = "ethernet "
            if "bond" in parent:
                parent_type = "bonding "

            statement = parent_type + parent + " vif " + str(vlan_id)

        elif iface_type == 'lacp':
            statement = "bonding " + interface

        elif iface_type == 'ethernet':
            statement = "ethernet " + interface

        else:
            ret = {"result": False, "comment": "Unsupported interface type."}

        ret = _is_marked_disabled(interface)

        if not ret.get('out') and not force:
            ret = {
                "result": False,
                "comment": "Interface not marked as disabled in REDIS. Use force=true to commit anyway.",
            }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="delete interface {{ statement }} disable",
                    test=test,
                    debug=debug,
                    commit_comment="enable interface " + interface,
                    statement=statement,
                    interface=interface,
                )
            )
            # force means it didn't have the mark anyway.
            if not force and not test:
                _remove_disable_mark(interface)

    return ret


def disable(interface, test=False, debug=False, force=False):
    """
    Disable a salt managed interface. The interface must exist in netdb.

    :param interface: The name of the tunnel to be disabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for a tunnel marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if tunnel is successfully disabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1 ethernet.disable eth1
        salt sin1 ethernet.disable eth1 test=True
        salt sin1 ethernet.disable bond0.902 force=False

    """
    name = 'disable_ethernet'
    ret = {"result": False, "comment": "Interface does not exist on selected router."}

    if not interface:
        ret = {"result": False, "comment": "No interface selected."}

    ret_ifaces = _get_ethernet()
    if not ret_ifaces.get('result'):
        return ret_ifaces

    ifaces = ret_ifaces.get('out')

    if interface not in ifaces.keys():
        ret = {"result": False, "comment": "Interface not found on this router."}
    else:
        iface_type = ifaces[interface]['type']
        statement = ''

        if iface_type == 'vlan':
            vlan_id = ifaces[interface]['vlan']['id']
            parent = ifaces[interface]['vlan']['parent']

            parent_type = "ethernet "
            if "bond" in parent:
                parent_type = "bonding "

            statement = parent_type + parent + " vif " + str(vlan_id)

        elif iface_type == 'lacp':
            statement = "bonding " + interface

        elif iface_type == 'ethernet':
            statement = "ethernet " + interface

        else:
            ret = {"result": False, "comment": "Unsupported interface type."}

        ret = _is_marked_disabled(interface)

        if ret.get('out') and not force:
            ret = {
                "result": False,
                "comment": "Interface is already marked disabled in REDIS. Use force=true to commit anyway.",
            }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="set interface {{ statement }} disable",
                    test=test,
                    debug=debug,
                    commit_comment="disable interface " + interface,
                    statement=statement,
                    interface=interface,
                )
            )
            # force means it didn't have the mark anyway.
            if not force and not test:
                _mark_disabled_interface(interface)

    return ret


def display(type='ethernet'):
    """
    Show the router's tunnels. This call is a wrapper around net.cli.

    A list of the router's salt managed tunnels is also displayed in the comment.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface information returned; false otherwise
       * comment: (str) A list of salt managed tunnels

    CLI Example::

    .. code-block:: bash

        salt sin1 ethernet.display

    """
    ret_ifaces = _get_ethernet()

    if type not in ['ethernet', 'lag']:
        return {"result": False, "comment": "unsupported interface type."}

    if type == 'lag':
        type = 'bonding'

    ret = __salt__['net.cli']("show interface " + type)

    disabled_ifaces = _get_disabled_interfaces()['out']

    iface_fmt = "{0:30} {1:20} {2:20}"
    if ret_ifaces['result']:
        ifaces = ret_ifaces['out']
        iface_list = []
        for interface, iface_data in ifaces.items():
            disabled = ''
            if interface in disabled_ifaces:
                disabled += "disabled"

            data = iface_fmt.format(interface, iface_data.get('datasource'), disabled)
            iface_list.append(data)

        comment_base = (
            iface_fmt.format("salt managed interfaces", "datasource", "") + "\n---\n"
        )
        ret['comment'] = comment_base + '\n'.join(iface_list)
    else:
        ret['comment'] = "netdb API is down"

    return ret


def apply_pni(interfaces, test=False, debug=False):
    """
    Apply a single interface to device. Uses same template as state.apply ethernet

    :param interfaces: comma separated list of interfaces to apply
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interfaces found in column and applied; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1 ethernet.apply_pni eth5,eth6 test=True
        salt sin1 ethernet.apply_pni interfaces=eth5,eth6
        salt sin1 ethernet.apply_pni eth6

    """
    name = 'apply_pni'

    ret = {'result': False}

    if not isinstance(test, bool):
        return {"result": False, "comment": "test option only accepts true or false."}

    if not isinstance(debug, bool):
        return {"result": False, "comment": "debug option only accepts true or false."}

    ethernet = generate()

    interfaces = interfaces.split(',')

    pni = {'comment': 'generated interfaces', 'result': False}

    for iface, data in ethernet['out'].items():
        if iface in interfaces:
            if not pni.get('out'):
                pni['out'] = {}
                pni['result'] = True
            pni['out'][iface] = data
            interfaces.remove(iface)

    if interfaces:
        return {
            'result': False,
            'out': interfaces,
            'comment': 'Interfaces not found',
        }

    if pni['result']:
        ret.update(
            __salt__['net.load_template'](
                'salt://ethernet/templates/vyos.jinja',
                test=test,
                debug=debug,
                commit_comment="Apply interfaces",
                data=pni,
            )
        )

    return ret
