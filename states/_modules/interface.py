import logging
from socket import inet_aton
from struct import unpack

from salt.exceptions import SaltException

__virtualname__ = "interface"

logger = logging.getLogger(__file__)

_COLUMN = 'interface'


def __virtual__():
    return __virtualname__


def _ip2long(ip: str) -> int:
    """
    Convert an IP string to long
    """
    return unpack("!L", inet_aton(ip))[0]


def get_vyos_ethernet() -> dict:
    """
    Generate dictionary for "state.apply ethernet". This call takes no arguments.

    :return: a dictionary consisting of all VyOS ethernet interfaces with VyOS keys added.

    CLI Example::

    .. code-block:: bash

        salt sin1 ethernet.get_vyos_interfaces

    """

    def _add_vyos_keys(interface, settings):
        """
        Accept a settings dictionary associated with an interface column key and add VyOS
        specific settings to it.
        """
        match (settings['type']):
            case 'ethernet':
                settings['vyos_type'] = 'ethernet'

            case 'lacp':
                settings['vyos_type'] = 'bonding'

            case 'vlan':
                settings['vyos_type'] = 'vif'

                parent = settings['vlan']['parent']

                if parent.startswith('bond'):
                    parent_vyos_type = 'bonding'

                elif parent.startswith('eth'):
                    parent_vyos_type = 'bonding'

                else:
                    raise SaltException(
                        f'{interface}: unsupported vlan parrent interface type {parent}!'
                    )

                settings['vlan']['parent_vyos_type'] = parent_vyos_type

            case _:
                raise SaltException(f'{interface}: unsupported interface type!')

        return settings

    return {
        interface: _add_vyos_keys(interface, settings)
        for interface, settings in __salt__['column.pull'](_COLUMN).items()
        if interface.startswith('bond') or interface.startswith('eth')
    }


def get_vyos_tunnels() -> dict:
    """
    Generate dictionary for "state.apply tunnels". This call takes no arguments.

    :return: a dictionary containing all tunnels found in the interface column with VyOS
             tunnel kays added.

    CLI Example::

    .. code-block:: bash

        salt sin1 tunnel.get_vyos_tunnels

    """

    def _vyos_tunnel_keys(settings: dict) -> dict:
        """
        VyOS does not accept octet encoded tunnels. Convert them to longs and add them in
        a new key.
        """
        if key := settings.get('key'):
            settings['key_vyos'] = _ip2long(key)

        return settings

    return {
        interface: _vyos_tunnel_keys(settings)
        for interface, settings in __salt__['column.pull'](_COLUMN).items()
        if interface.startswith('tun')
    }


def get_vyos_loopbacks() -> dict:
    """
    Generate dictionary for "state.apply loopback". This call takes no arguments.

    :return: a dictionary consisting of the loopback interfaces from the interfaces
             column.

    CLI Example::

    .. code-block:: bash

        salt sin1 loopback.get_loopbacks

    """

    return {
        interface: settings
        for interface, settings in __salt__['column.pull'](_COLUMN).items()
        if interface.startswith('dum')
    }
