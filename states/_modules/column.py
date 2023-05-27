import logging

__virtualname__ = "column"

logger = logging.getLogger(__file__)

def __virtual__():
    return __virtualname__


def _netdb_pull(column):
    netdb_answer = __salt__['netdb.get_column'](column)

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        netdb_answer.update({ 'error': True })

    return netdb_answer


def _netdb_columns():
    netdb_answer = __salt__['netdb.list_columns']()

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        netdb_answer.update({ 'error': True })

    return netdb_answer


def _get(column, delimiter=':'):
    c = column.split(delimiter)

    netdb_answer = _netdb_pull(c.pop(0))

    if netdb_answer.get('error'):
        return { 
                'comment' : netdb_answer.get('comment'),
                'result'  : False,
               }

    unwind = netdb_answer['out'].get(__grains__['id'])
    for i in range(0, len(c)):
        unwind = unwind.get(c[i])
        if not isinstance(unwind, dict):
            if i < len(c) - 1:
                return None
            break

    return unwind


def ls():
    """
    Calls netdb for a list of available columns and returns this list.

    CLI Example::

    .. code-block:: bash

        salt sin1 column.ls

    """
    netdb_answer = _netdb_columns()

    if netdb_answer.get('error'):
        return netdb_answer

    return netdb_answer['out']


def get(column, delimiter=':'):
    """
    Retrieves a column from netdb for the device. Netdb 'config' endpoint is
    called so netdb will return the fully built configuration for this device
    instead of a raw column.

    The value can also represent a value in a nested dict using a ":" delimiter
    for the dict. This means that if a dict in the column looks like this::

    {'device': {'location': 'Singapore'}}

    To retrieve the value associated with the ``location`` key in the ``device``
    dict this key can be passed as::

    device:location

    delimiter
        Specify an alternate delimiter to use when traversing a nested dic

    CLI Example::

    .. code-block:: bash

        salt sin1 column.get interface
        salt sin1 column.get device:location

    """
    if isinstance(delimiter, int):
        delimiter = str(delimiter)
    elif not isinstance(delimiter, str):
        return  {
                'result'  : False,
                'error'   : True,
                'comment' : 'delimiter must be a string or char',
                }

    ret = _get(column, delimiter)
    if not ret or (isinstance(ret, dict) and ret.get('result') == False):
        return []

    return ret


def keys(column, delimiter=':'):
    """
    Attempt to retrieve a list of keys from the named value from column.

    The value can also represent a value in a nested dict using a ":" delimiter
    for the dict, similar to how column.get works.

    delimiter
        Specify an alternate delimiter to use when traversing a nested dic

    CLI Example::

    .. code-block:: bash

        salt sin2 column.keys device
        salt sin2 column.keys interface:tun372

    """
    if isinstance(delimiter, int):
        delimiter = str(delimiter)
    elif not isinstance(delimiter, str):
        return  {
                'result'  : False,
                'error'   : True,
                'comment' : 'delimiter must be a string or char',
                }

    ret = _get(column, delimiter)

    if isinstance(ret, dict):
        if ret.get('result') == False:
            return []
        return list(ret.keys())
    else:
        return []


def item(*arg, **kwarg):
    """
    Return one or more columns from netdb.

    delimiter
        Specify an alternate delimiter to use when traversing a nested dic

    CLI Example::

    .. code-block:: bash

        salt sin1 column.item device firewall
        salt sin2 column.item igp

    """
    out = {}
    delimiter = kwarg.pop('delimiter', ':')

    if isinstance(delimiter, int):
        delimiter = str(delimiter)
    elif not isinstance(delimiter, str):
        return  {
                'result'  : False,
                'error'   : True,
                'comment' : 'delimiter must be a string or char',
                }

    for column in arg:
        data = _get(column, delimiter)

        if not data or (isinstance(data, dict) and data.get('result') == False):
            out[column] = []
        else:
            out[column] = data

    return out
