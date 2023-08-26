import logging
from .netdb import get_column, list_columns

logger = logging.getLogger(__file__)

def list():
    netdb_answer = list_columns()

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        netdb_answer.update({ 'error': True })

    return netdb_answer


def get(column, delimiter=':'):
    """
    Retrieves a column from netdb for the device. Used by column module
    'get', 'items' and 'keys' functions.
    """
    router = __grains__['node_name']

    c = column.split(delimiter)

    netdb_answer = get_column(c.pop(0))
    if not netdb_answer['result'] or 'out' not in netdb_answer:
        return { 
                'comment' : netdb_answer.get('comment'),
                'result'  : False,
                'error'   : True,
               }

    unwind = netdb_answer['out'].get(router)
    for i in range(0, len(c)):
        unwind = unwind.get(c[i])
        if not isinstance(unwind, dict):
            if i < len(c) - 1:
                return None
            break

    return unwind


def pull(column):
    """
    Retrieves a column from netdb for the device. None is returned in case of
    error or no result. Intended for use by salt state apply pipeline.
    """
    router = __grains__['node_name']

    netdb_answer = get_column(column)

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        return { 
                'comment' : netdb_answer.get('comment'),
                'result'  : False,
                'error'   : True,
               }

    return {
            'comment' : netdb_answer.get('comment'),
            'out'     : netdb_answer['out'].get(router),
            'result'  : True,
            }
