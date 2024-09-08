import logging

from netdb_util_api import NetdbUtilAPI

__virtualname__ = "repo_yaml"

_ENDPOINT = 'connectors/repo/{}'

log = logging.getLogger(__file__)


def __virtual__():
    return __virtualname__


def generate_column(column):
    """
    Show generated column data for repo_yaml column repository
    in netdb format.

    :param column: name of column to generate
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of devices in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run repo_yaml.generate_column bgp

    """
    return NetdbUtilAPI(__salt__['pillar.show_pillar']()).get(_ENDPOINT.format(column))


def reload_column(column, verbose=False):
    """
    Clear all repo_yaml column data from a netdb column and load
    a fresh version from repository

    :param column: name of column to generate
    :param verbose: show generated column data as well
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if data returned; false otherwise
       * out: a dict of devices in netdb format

    CLI Example::

    .. code-block:: bash

        salt-run repo_yaml.reload_column bgp

    """
    ret = NetdbUtilAPI(__salt__['pillar.show_pillar']()).post(_ENDPOINT.format(column))

    return True if ret['result'] and not ret['error'] and not verbose else ret
