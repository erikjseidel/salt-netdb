# -*- coding: utf-8 -*-

import logging
import copy

__virtualname__ = "ethernet"

log = logging.getLogger(__file__)

_COLUMN = 'interface'

# Disabled tunnels stored in this redis key.
_REDIS_KEY = 'ethernet_disabled'


def __virtual__():
    return __virtualname__


def _netdb_pull():
    router = __grains__['id']
    netdb_answer =  __salt__['netdb.get_column'](_COLUMN)

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        return netdb_answer

    interfaces = netdb_answer['out']

    ethernet = {}

    for iface, iface_data in interfaces[router]['interfaces'].items():
        if iface.startswith('eth') or iface.startswith('bond'):
            ethernet[iface] = iface_data

    return { 'result': True, 'out': ethernet }

def _enable_interface(interface, disable=False, test=True):
    return __salt__['netdb.enable_interface'](_COLUMN, interface, disable=disable, test=test)


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

        salt sin1-proxy ethernet.generate

    """
    ret_ethernet = _netdb_pull()
    if not ret_ethernet['result']:
        return ret_ethernet

    ifaces = ret_ethernet['out']

    ret = {'out': {}, 'result': False, 'error': False}

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
                return {'result': False, 'comment': interface + ": unsupported vlan parrent interface type!"}
        else:
            return {'result': False, 'comment': interface + ": unsupported interface type!"}

    ret.update({'result': True, 'out': ifaces})

    return ret


def enable(interface, test=False, permanent=False, debug=False, force=False):
    """
    Enable a salt managed ethernet, vlan or bundle interface. The interface must exist in 
    netdb.

    :param interface: The name of the interface to be enabled
    :param test: True for dry-run. False to apply on the router.
    :param permanent: True to update netdb in addition to router and local REDIS
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for a tunnel not marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface is successfully enabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy ethernet.enable bond0.17
        salt sin1-proxy ethernet.enable bond0.15 test=True
        salt sin1-proxy ethernet.enable eth1 force=False

    """
    name = 'enable_ethernet'
    ret = {"result": False, "comment": "Interface does not exist on selected router."}

    if not interface:
        ret = {"result": False, "comment": "No interface selected."}

    ret_ifaces = _netdb_pull()
    if not ret_ifaces['result']:
        return ret_ifaces

    ifaces = ret_ifaces['out']

    if interface not in ifaces.keys():
        ret = {"result": False, "comment": "Interface not found on this router."}
    else:
        iface_type = ifaces[interface]['type']
        statement = ''

        if iface_type == 'vlan':
            vlan_id = ifaces[interface]['vlan']['id']
            parent  = ifaces[interface]['vlan']['parent']

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

        if not ret['out'] and not force:
            ret = {
                "result": False,
                "comment": "Interface not marked as disabled in REDIS. Use force=true to commit anyway."
                }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="delete interface {{ statement }} disable",
                    test=test,
                    debug=debug,
                    commit_comment = "enable interface " + interface,
                    statement=statement,
                    interface=interface,
                )
            )
            # force means it didn't have the mark anyway.
            if not force and not test:
                _remove_disable_mark(interface)

            if permanent:
                result = _enable_interface(interface, disable=False, test=test)
                ret['comment']     += ' Permanent (netdb) disable requested.'
                ret['netdb'] = { 
                        'result'  : result['result'],
                        'comment' : result['comment'],
                        }

    return ret


def disable(interface, test=False, permanent=False, debug=False, force=False):
    """
    Disable a salt managed interface. The interface must exist in netdb.

    :param interface: The name of the tunnel to be disabled
    :param test: True for dry-run. False to apply on the router.
    :param permanent: True to update netdb in addition to router and local REDIS
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for a tunnel marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if tunnel is successfully disabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy ethernet.disable eth1
        salt sin1-proxy ethernet.disable eth1 test=True
        salt sin1-proxy ethernet.disable bond0.902 force=False

    """
    name = 'disable_ethernet'
    ret = {"result": False, "comment": "Interface does not exist on selected router."}

    if not interface:
        ret = {"result": False, "comment": "No interface selected."}

    ret_ifaces = _netdb_pull()
    if not ret_ifaces['result']:
        return ret_ifaces

    ifaces = ret_ifaces['out']

    if interface not in ifaces.keys():
        ret = {"result": False, "comment": "Interface not found on this router."}
    else:
        iface_type = ifaces[interface]['type']
        statement = ''

        if iface_type == 'vlan':
            vlan_id = ifaces[interface]['vlan']['id']
            parent  = ifaces[interface]['vlan']['parent']

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

        if ret['out'] and not force:
            ret = {
                "result": False,
                "comment": "Interface is already marked disabled in REDIS. Use force=true to commit anyway."
                }
        else:
            ret.update(
                __salt__['net.load_template'](
                    template_name=name,
                    template_source="set interface {{ statement }} disable",
                    test=test,
                    debug=debug,
                    commit_comment = "disable interface " + interface,
                    statement=statement,
                    interface=interface,
                )
            )
            # force means it didn't have the mark anyway.
            if not force and not test:
                _mark_disabled_interface(interface)

            if permanent:
                result = _enable_interface(interface, disable=True, test=test)
                ret['comment']     += ' Permanent (netdb) disable requested.'
                ret['netdb'] = { 
                        'result'  : result['result'],
                        'comment' : result['comment'],
                        }

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

        salt sin1-proxy tunnel.display

    """
    ret_ifaces = _netdb_pull()

    ret = {"result": False, "comment": "unsupported operating system."}

    if type not in ['ethernet', 'lag']:
        return {"result": False, "comment": "unsupported interface type."}

    if type == 'lag':
        type = 'bonding'

    if (
        __grains__['os'] == "vyos"
       ):

        ret.update(
            __salt__['net.cli'](
                "show interface " + type,
            )
        )
    
    disabled_ifaces = _get_disabled_interfaces()['out']

    if ret_ifaces['result']:
        ifaces = ret_ifaces['out'].keys()
        iface_list = []
        for interface in ifaces:
            data = interface
            if interface in disabled_ifaces:
                data += "\t[disabled]"
            iface_list.append(data)

        ret['comment'] = "salt managed interfaces:\n--- \n" + '\n'.join( iface_list )
    else:
        ret['comment'] = "netdb API is down"

    return ret
