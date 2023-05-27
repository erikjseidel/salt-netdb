
import salt.utils.http
import json

__virtualname__ = 'netdb'

_PILLAR = 'netdb'

def __virtual__():
    if ( _PILLAR in __pillar__.keys() ):
        return __virtualname__
    else:
        return ( False, 'netdb configuration pillar not found.' )


def get_column(column):
    """
    Return a column for router grains.id from netdb.

    :param key: name of the entry list to query
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if router has entries for key `key'; false otherwise
       * comment: (str) (only if return: False) an explanation
       * error: (bool) True if an API error occured (such as connection timeout)

    """
    router = __grains__['id']
    netdb = __pillar__[_PILLAR]

    url = netdb['url'] + column + '/' + router + '/config'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    method = "GET"
    resp = salt.utils.http.query(
        url=url, method=method, header_dict=headers, verify_ssl=False,
        cert = [ netdb['key'], netdb['key'] ]
    )

    if 'body' in resp:
        return json.loads(resp['body'])
    else:
        return { 'result': False, 'error': True, 'comment': 'netdb api error: ' +  resp['error'] }


def _query(column, filt=None):
    netdb = __pillar__[_PILLAR]

    url = netdb['url'] + column

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    resp = salt.utils.http.query(
        url=url, method='GET', header_dict=headers, verify_ssl=False, data=json.dumps(filt),
        cert = [ netdb['key'], netdb['key'] ]
    )

    if 'body' in resp:
        return json.loads(resp['body'])
    else:
        return { 'result': False, 'error': True, 'comment': 'netdb api error: ' +  resp['error'] }


def _update(column, data, test=False):
    netdb = __pillar__[_PILLAR]

    url = netdb['url'] + column
    if test:
        url += '/validate'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    resp = salt.utils.http.query(
        url=url, method='PUT', header_dict=headers, verify_ssl=False, data=json.dumps(data),
        cert = [ netdb['key'], netdb['key'] ]
    )

    if 'body' in resp:
        return json.loads(resp['body'])
    else:
        return { 'result': False, 'error': True, 'comment': 'netdb api error: ' +  resp['error'] }


def update(column, data, test=True):
    netdb_answer = _update(column, data=data, test=test)
    if netdb_answer['result']:
        netdb_answer.update({'out': data})

    return netdb_answer


def enable_interface(column, interface, disable=False, test=True):
    device = __grains__['id']

    filt = [ device, None, None, interface ]
    netdb_answer = _query(column, filt = filt)
    if not netdb_answer['result']:
        return netdb_answer

    assert 'out' in netdb_answer
    iface = netdb_answer['out']

    assert device in iface, interface in iface[device]['interfaces']
    if disable:
        iface[device]['interfaces'][interface]['disabled'] = True
    else:
        iface[device]['interfaces'][interface].pop('disabled', None)

    return update(column, iface, test)


def list_columns():
    """
    Return a list of netdb columns.

    :param key: name of the entry list to query
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if router has entries for key `key'; false otherwise
       * comment: (str) (only if return: False) an explanation
       * error: (bool) True if an API error occured (such as connection timeout)

    """
    netdb = __pillar__[_PILLAR]
    url = netdb['url'] + 'columns'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    method = "GET"
    resp = salt.utils.http.query(
        url=url, method=method, header_dict=headers, verify_ssl=False,
        cert = [ netdb['key'], netdb['key'] ]
    )

    if 'body' in resp:
        return json.loads(resp['body'])
    else:
        return { 'result': False, 'error': True, 'comment': 'netdb api error: ' +  resp['error'] }
