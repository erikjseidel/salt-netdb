import requests, json

HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        }

def __virtual__():
    netdb_config = __opts__["netdb"] if "netdb" in __opts__ else None

    if netdb_config:
        url = netdb_config.get("util_url", None)
        if not url:
            return ( False, 'netdb util url not found' )
        else:
            return True

    return ( False, 'netdb config not found' )


def _get_netdb_config():
    return {
        "url":      __opts__["netdb"]["url"],
        "util_url": __opts__["netdb"]["util_url"],
        "key":      __opts__["netdb"].get("key"),
    }


def call_netdb_util(endpoint, data=None, params={}, method='GET', test=True):
    if method not in ['GET', 'POST', 'PUT', 'DELETE']:
        return {
                'result': False,
                'error': True,
                'comment': f'Internal runner error: {method} not allowed.'
                }

    if not params:
        params = {}

    netdb = _get_netdb_config()

    url = netdb['util_url'] + endpoint

    if not test:
        params['test'] = False

    key = None
    if netdb.get('key'):
        key = netdb['key']

    verify=False
    # Keep at default value in case of http.
    if url.startswith('http://'):
        verify=True

    resp = requests.request(
            url=url,
            method=method,
            headers=HEADERS,
            params=params,
            json=data,
            verify=verify,
            cert=key
            )

    if resp.status_code in [200, 422]:
        return resp.json()
    else:
        return {
                'result': False,
                'error': True,
                'comment': f'netdb api error: {resp.status_code} {resp.reason}'
                }
