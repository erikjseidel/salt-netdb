import logging
from .netdb import get_column, list_columns

logger = logging.getLogger(__file__)

def _netdb_pull(column):
    netdb_answer = get_column(column)

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        netdb_answer.update({ 'error': True })

    return netdb_answer


def list():
    netdb_answer = list_columns()

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        netdb_answer.update({ 'error': True })

    return netdb_answer


def get(column, delimiter=':'):
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


def pull(column):
    """
    Retrieves a column from netdb for the device. None is returned in case of
    error or no result. Intended for use by salt state apply pipeline.
    """

    netdb_answer = _netdb_pull(column)

    if netdb_answer.get('error') or not netdb_answer.get('out'):
        return { 
                'comment' : netdb_answer.get('comment'),
                'result'  : False,
                'error'   : True,
               }

    return {
            'comment' : netdb_answer.get('comment'),
            'out'     : netdb_answer['out'].get(__grains__['id']),
            'result'  : True,
            }
