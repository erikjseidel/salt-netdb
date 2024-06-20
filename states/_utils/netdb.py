import requests, json

_PILLAR = 'netdb'

_LOCAL = 'netdb_local'

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def get_grains(netdb, netdb_local):
    router = netdb['id'].upper()

    url = netdb['url'] + 'column/device/{}'.format(router)
    key = netdb.get('key')

    if netdb_local and netdb_local.get('enabled'):
        url = netdb_local['url'] + 'column/device/{}'.format(router)
        key = netdb_local.get('key')

    verify = False
    if url.startswith('http://'):
        verify = True

    resp = requests.get(url=url, headers=HEADERS, verify=verify, cert=key)

    if resp.status_code == 200:
        return resp.json()['out'][router]
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
    router = __grains__['node_name']
    netdb = __pillar__[_PILLAR]
    netdb_local = __pillar__.get(_LOCAL)

    endpoint = 'column/{column}/{device}'.format(column=column, device=router)

    url = netdb['url'] + endpoint
    key = netdb.get('key')

    if netdb_local and netdb_local.get('enabled'):
        url = netdb_local['url'] + endpoint
        key = netdb_local.get('key')

    verify = False
    if url.startswith('http://'):
        verify = True

    resp = requests.get(url=url, headers=HEADERS, verify=verify, cert=key)

    if resp.status_code in [200, 422]:
        return resp.json()
    else:
        return {
            'result': False,
            'error': True,
            'comment': f'netdb api error: {resp.status_code} {resp.reason}',
        }


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
    netdb_local = __pillar__.get(_LOCAL)

    url = netdb['url'] + 'column'
    key = netdb.get('key')

    if netdb_local and netdb_local.get('enabled'):
        url = netdb_local['url'] + 'column'
        key = netdb_local.get('key')

    verify = False
    if url.startswith('http://'):
        verify = True

    resp = requests.get(url=url, headers=HEADERS, verify=verify, cert=key)

    if resp.status_code == 200:
        return resp.json()
    else:
        return {
            'result': False,
            'error': True,
            'comment': f'netdb api error: {resp.status_code} {resp.reason}',
        }
