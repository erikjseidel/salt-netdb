
from pathlib import Path
import yaml, json

_COLUMNS=[ 'interface', 'igp', 'bgp', 'firewall', 'policy', 'device' ]

def _netdb_save(column, data=None, test=True):
    return __utils__['netdb_runner.save'](column, data, test)


def _netdb_update(column, data, test=True):
    return __utils__['netdb_runner.update'](column, data, test)


def _netdb_get(column, data=None):
    return __utils__['netdb_runner.get'](column, data = data)


def load_yaml(column, path, test=True, outputter=None, display_progress=False):
    """
    Bulk load configuration data from a YAML file. Only elements
    that do not exist will be loaded.

    :param column: device where interface is located
    :param path: location of YAML file to be loaded
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise

    CLI Example::

    .. code-block:: bash

        salt-run loader.load_yaml interface /foo/bar/interfaces.yaml 
        salt-run loader.load_yaml column=interface path=interfaces.yaml 

    """
    try:
        conf = yaml.safe_load(Path(path).read_text())
    except FileNotFoundError:
        return { 'result': False, 'error': True, 'comment': 'File not found.' }

    data = json.dumps(conf)

    return _netdb_save(column, data=conf, test=test)


def update_from_yaml(column, path, test=True, outputter=None, display_progress=False):
    """
    Bulk update configuration data from a YAML file. Only elements
    that do exist will be loaded.

    :param column: device where interface is located
    :param path: location of YAML file to be loaded
    :param test: set true to perform netdb update (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise

    CLI Example::

    .. code-block:: bash

        salt-run loader.update_from_yaml interface /foo/bar/interfaces.yaml 
        salt-run loader.update_from_yaml column=interface path=interfaces.yaml 

    """
    try:
        conf = yaml.safe_load(Path(path).read_text())
    except FileNotFoundError:
        return { 'result': False, 'error': True, 'comment': 'File not found.' }

    data = json.dumps(conf)

    return _netdb_update(column, conf, test)


def get_column (column, raw=False, outputter=None, display_progress=False):
    """
    Dump column configuration data to stdout

    :param column: column to dumped 
    :param raw: dump yaml to stdout (i.e. in order to save as a file
                can then be uploaded with update_from_yaml (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise

    CLI Example::

    .. code-block:: bash

        salt-run loader.get_column interface raw=true > interfaces.yaml 
        salt-run loader.get_column column=interface

    """
    if column not in _COLUMNS:
        return { 'result': False, 'comment': 'Invalid column' }

    netdb_answer = _netdb_get(column)

    if netdb_answer['result'] and raw:
        return yaml.dump(netdb_answer['out'])

    return netdb_answer


def query (column, set_id=None, category=None, family=None, 
                    element=None, raw=False, outputter=None, display_progress=False):
    """
    Query netdb by element identifiers and print results to stdout.

    :param column: column to be queried (required)
    :param set_id: configuration set id or device id in case of device
    :param category: column configuration category
    :param family: address family identifier (i.e. 'ipv4' or 'ipv6')
    :param element: element id
    :param raw: dump yaml to stdout (i.e. in order to save as a file
                can then be uploaded with update_from_yaml (defaults to false)
    :return: a dictionary consisting of the following keys:

       * result: (bool) true if successful; false otherwise

    CLI Example::

    .. code-block:: bash

        salt-run loader.query interface element=tun376 raw=true > interfaces.yaml 
        salt-run loader.query column=interface set_id=sin3 element=tun376

    """
    if set_id and not set_id.startswith('_'):
        set_id = set_id.upper()

    if column not in _COLUMNS:
        return { 'result': False, 'comment': 'Invalid column' }

    filt = [ set_id, category, family, element ]

    netdb_answer = _netdb_get(column, data = filt)

    if netdb_answer['result'] and raw:
        return yaml.dump(netdb_answer['out'])

    return netdb_answer
