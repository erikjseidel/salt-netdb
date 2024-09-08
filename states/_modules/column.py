from typing import Union, Any
import logging

__virtualname__ = "column"

from salt.exceptions import SaltException

from netdb_api import NetdbAPI
from exceptions.netdb_exceptions import ColumnNotFoundException

logger = logging.getLogger(__file__)


def __virtual__():
    return __virtualname__


def ls() -> list:
    """
    Calls netdb for a list of available columns and returns this list.

    CLI Example::

    .. code-block:: bash

        salt sin1 column.ls

    """
    return NetdbAPI(__pillar__).list_columns()['out']


def get(column: str, delimiter: str = ':') -> Any:
    """
    Retrieves a column from netdb for the device.

    The value can also represent a value in a nested dict using a ":" delimiter
    for the dict. This means that if a dict in the column looks like this::

    {'device': {'location': 'Singapore'}}

    To retrieve the value associated with the ``location`` key in the ``device``
    dict this key can be passed as::

    device:location

    delimiter
        Specify an alternate delimiter to use when traversing a nested dict

    CLI Example::

    .. code-block:: bash

        salt sin1 column.get interface
        salt sin1 column.get device:location

    """
    if isinstance(delimiter, int):
        delimiter = str(delimiter)

    elif not isinstance(delimiter, str):
        return {
            'result': False,
            'comment': 'delimiter must be a string or char',
        }

    c = column.split(delimiter)
    column = c.pop(0)

    try:
        unwind = NetdbAPI(__pillar__).get_column(__grains__['node_name'], column)
    except ColumnNotFoundException:
        # We follow pillar convention of returning an empty list if no column found
        return []

    for i, elem in enumerate(c):
        unwind = unwind.get(elem)  # type: ignore
        if not isinstance(unwind, dict):
            if i < len(c) - 1:
                return None
            break

    return unwind or []


def pull(column: str) -> dict:
    """
    Retrieves a raw column from netdb for the device in a manner suitable for state
    applies. No column filtering is done. In case of non-existent or empty column a
    a SaltException is raised.

    CLI Example::

    .. code-block:: bash

        salt sin1 column.pull interface

    """
    try:
        ret = NetdbAPI(__pillar__).get_column(__grains__['node_name'], column)
    except ColumnNotFoundException as e:
        raise SaltException(str(e)) from e

    if not ret:
        raise SaltException(f'{column}: Empty column returned')

    return ret


def keys(column: str, delimiter: str = ':') -> Union[list, dict]:
    """
    Attempt to retrieve a list of keys from the named value from column.

    The value can also represent a value in a nested dict using a ":" delimiter
    for the dict, similar to how column.get works.

    delimiter
        Specify an alternate delimiter to use when traversing a nested dict

    CLI Example::

    .. code-block:: bash

        salt sin2 column.keys device
        salt sin2 column.keys interface:tun372

    """
    ret = get(column, delimiter)

    if isinstance(ret, dict):
        return ret if ret.get('result') is False else list(ret.keys())

    return []


def item(*args, **kwargs) -> Union[dict, list]:
    """
    Return one or more columns from netdb.

    delimiter
        Specify an alternate delimiter to use when traversing a nested dict

    CLI Example::

    .. code-block:: bash

        salt sin1 column.item device firewall
        salt sin2 column.item igp

    """
    out = {}
    delimiter = kwargs.pop('delimiter', ':')

    for column in args:
        out[column] = get(column, delimiter)
        if isinstance(out[column], dict) and out[column].get('result') is False:
            #
            # False result means that there was an issue with the delimiter. Return the
            # error message.
            #
            return out[column]

        if not out[column] or (
            isinstance(out[column], dict) and out[column].get('result') is False
        ):
            out[column] = []

    return out
