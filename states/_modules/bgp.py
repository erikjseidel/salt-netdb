# -*- coding: utf-8 -*-

import logging
import copy

__virtualname__ = "bgp"

log = logging.getLogger(__file__)

_PILLAR = 'znsl_bgp'
#  bgp disabled peers stored in this redis key.
_REDIS_KEY = 'bgp_disabled'

def __virtual__():
    if ( _PILLAR in __pillar__.keys() ):
        return __virtualname__
    else:
        return ( False, 'BGP not enabled or not salt managed on this router. Module not loaded.' )


def _get_peers():
    """
    Returns salt managed BGP peers on router plus the address families configured for each peer
    """
    bgp = __pillar__[_PILLAR]

    peer_groups = {}
    neighbors = {}

    """ Load peer group data, needed to provide list of families for each neighbor
    """
    for config_group, data in bgp.items():
        if 'peer_groups' in data.keys():
            for peer_group, peer_group_data in data['peer_groups'].items():
                peer_groups[peer_group] = peer_group_data

    for config_group, data in bgp.items():
        if 'neighbors' in data.keys():
            for neighbor, neighbor_data in data['neighbors'].items():
                neighbors[neighbor] = neighbor_data

                """ provide a list of families; used by disable / enable functions
                    do determine where to add REJECT-ALL policies
                """
                if 'peer_group' in neighbor_data.keys():
                    pg = neighbor_data['peer_group']
                    neighbors[neighbor]['families'] = list(peer_groups[pg]['family'].keys())

                #  salt managed neighbors should always be members of a peer group
                #  as such we should never reach this point
                else:
                    neighbors[neighbor]['families'] = []

    ret = { 'result': True, 'out': neighbors }

    if not neighbors:
        ret = { 'result': False, 'comment': 'no salt managed peers found', 'out': neighbors }

    return ret


def _is_marked_disabled(peer):
    """
    Checks if a BGP peer is disabled. Wrapper around generic net_redis entry functions.
    """
    return __salt__['net_redis.check_entry'](_REDIS_KEY, peer)


def _remove_disable_mark(peer):
    """
    Removes a BGP peer is in the disabled list. Wrapper around generic net_redis entry functions.
    """
    bgp_peers = _get_peers()['out']

    if not peer:
        return {"result": False, "comment": "No BGP peer selected."}

    if peer not in bgp_peers.keys():
        return {"result": False, "comment": "BGP peer not found."}

    return __salt__['net_redis.remove_entry'](_REDIS_KEY, peer)


def _mark_disabled_peer(peer):
    """
    Adds a BGP peer to the disabled list. Wrapper around generic net_redis entry functions.
    """
    bgp_peers = _get_peers()['out']

    if not peer:
        return {"result": False, "comment": "No BGP peer selected."}

    if peer not in bgp_peers.keys():
        return {"result": False, "comment": "BGP peer not found."}

    return __salt__['net_redis.add_entry'](_REDIS_KEY, peer)


def _get_disabled_peers():
    """
    Retrieves list of BGP disabled peers. Wrapper around generic net_redis entry functions.
    """
    return __salt__['net_redis.get_entries'](_REDIS_KEY)


def generate():
    """
    Generate dictionary for "state.apply bgp". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy bgp.generate

    """

    bgp = __pillar__[_PILLAR]

    ret = {'out': {}, 'result': False, 'error': False}

    if not (bgp):
        ret.update(
            {
                'comment': 'Failed to get policy data',
                'error': True,
            }
        )
        return ret
    
    bgp_out = copy.deepcopy(bgp)

    ret.update({'result': True, 'out': bgp_out})

    return ret


def enable(peer, test=False, debug=False, force=False):
    """
    Remove REJECT-ALL import and export filters on a salt managed BGP peer. The peer must
    exist in the router's bgp pillar.

    :param peer: The IP address of the BGP peer to be enabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for a peer marked as enabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if a peer is successfully enabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy bgp.enable 23.181.64.4
        salt sin1-proxy bgp.enable 23.181.64.4 test=True
        salt sin1-proxy bgp.enable 23.181.64.4 force=True

    """

    peers = _get_peers()['out']

    name = 'bgp_enable'

    ret = {}

    if not isinstance(force, bool):
        return {"result": False, "comment": "force option only accepts true or false."}

    if not peer:
        return {"result": False, "comment": "No BGP peer selected."}

    if peer not in peers.keys():
        ret = {"result": False, "comment": "BGP peer not found."}
    else:
        ret = _is_marked_disabled(peer)

        if not ret['out'] and not force:
            ret = {
                "result": False,
                "comment": "BGP peer not marked as disabled in REDIS. Use force=true to commit anyway."
                }
        else:
            ret.update(
                __salt__['net.load_template'](
                    'salt://templates/bgp/enable.jinja',
                    test=test,
                    debug=debug,
                    commit_comment = "enable BGP peer " + peer,
                    peer=peer,
                )
            )
            # force means its already marked.
            if not force and not test:
                _remove_disable_mark(peer)

    return ret


def disable(peer, test=False, debug=False, force=False):
    """
    Set REJECT-ALL import and export filters on a salt managed BGP peer. The peer must
    exist in the router's bgp pillar.

    :param peer: The IP address of the BGP peer to be disabled
    :param test: True for dry-run. False to apply on the router.
    :param debug: True to show additional debugging information
    :param force: Force a commit to the router for a peer marked as disabled in REDIS
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if a peer is successfully disabled; false otherwise
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy bgp.disable 23.181.64.4
        salt sin1-proxy bgp.disable 23.181.64.4 test=True
        salt sin1-proxy bgp.disable 23.181.64.4 force=True

    """

    peers = _get_peers()['out']

    name = 'bgp_disable'

    ret = {}

    if not isinstance(force, bool):
        return {"result": False, "comment": "force option only accepts true or false."}

    if not peer:
        return {"result": False, "comment": "No BGP peer selected."}

    if peer not in peers.keys():
        ret = {"result": False, "comment": "BGP peer not found."}
    else:
        ret = _is_marked_disabled(peer)

        families = peers[peer]['families']

        if ret['out'] and not force:
            ret = {
                "result": False,
                "comment": "BGP peer already marked as disabled in REDIS. Use force=true to commit anyway."
                }
        else:
            ret.update(
                __salt__['net.load_template'](
                    'salt://templates/bgp/disable.jinja',
                    test=test,
                    debug=debug,
                    commit_comment = "disable BGP peer " + peer,
                    peer=peer,
                    families=families,
                )
            )
            # force means its already marked.
            if not force and not test:
                _mark_disabled_peer(peer)

    return ret

def summary(family='both'):
    """
    Show the router's BGP peers. This call is a wrapper around net.cli.

    A list of the router's salt managed BGP peers is also displayed in the comment.

    :param family: Show peers with 'ipv4', 'ipv6' families configured or 'both' (default)
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if interface information returned; false otherwise
       * comment: (str) A list of salt managed BGP peers

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy bgp.summary

    """

    peers = _get_peers()['out']

    name = 'bgp_summary'

    ret = {"result": False, "comment": "unsupported operating system."}

    if family not in ['ipv4', 'ipv6', 'both']:
        return {"result": False, "comment": "unsupported address family."}

    if ( __grains__['os'] == "vyos" ):
        command = 'show bgp summary'

        if family == 'ipv4':
            command = 'show ip bgp summary'
        elif family == 'ipv6':
            command = 'show ipv6 bgp summary'

        ret.update(
            __salt__['net.cli'](
                command,
            )
        )
    else:
        return ret

    disabled_peers = _get_disabled_peers()['out']

    peer_list = []
    for peer, peer_data in peers.items():
        if family == 'both' or family in peer_data['families']:
            data = "{0:30} {1:20}".format(peer, peer_data['peer_group'])
            if peer in disabled_peers:
                data += "\t[disabled]"
            peer_list.append(data)

    ret['comment'] = "salt managed peers:\n--- \n" + '\n'.join( peer_list  )

    return ret
