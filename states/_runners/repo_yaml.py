import logging

__virtualname__ = "repo_yaml"

_REPO_YAML_UTIL_NAME = 'repo'

log = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__


def _call_repo_yaml_util(function, data=None, params=None, method='GET', test=True):
    endpoint = _REPO_YAML_UTIL_NAME + '/' + function

    return __utils__['netdb_runner.call_netdb_util'](endpoint, data=data, params=params, method=method, test=test)


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
    params = {
            'column' : column,
            }

    return _call_repo_yaml_util('generate_column', params=params)


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
    params = {
            'column' : column,
            }

    ret = _call_repo_yaml_util('reload_column', params=params, method='POST')

    if ret['result'] and not ret['error'] and not verbose:
        return { 'result': True }

    return ret
