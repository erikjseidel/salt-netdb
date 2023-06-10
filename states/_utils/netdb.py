import salt.utils.http
import json

_PILLAR = 'netdb'

def get_grains(pillar):
    router = pillar['id'].upper()

    url = pillar['url'] + 'device' + '/' + router

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    method = "GET"
    resp = salt.utils.http.query(
        url=url, method=method, header_dict=headers, verify_ssl=False,
        cert = [ pillar['key'], pillar['key'] ]
    )

    if 'body' in resp:
        return json.loads(resp['body'])['out'][router]
    else:
        return {}


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
