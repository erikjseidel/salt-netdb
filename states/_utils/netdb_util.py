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
        "key":      __opts__["netdb"]["key"],
    }


def call_netdb_util(endpoint, data=None, params=None, method='GET', test=True):
    netdb = _get_netdb_config()

    url = netdb['util_url'] + endpoint + '?'
    if not test:
        url += 'test=false&'

    if params:
        for k, v in params.items():
            url += f'{k}={v}&' 

    # prettify url
    if url[-1] in ['?', '&']:
        url = url[:-1]

    json = None
    if data:
        json = json.dumps(data)

    if method == 'GET':
        resp = requests.get(url=url, headers=HEADERS, data=json, verify=False, cert=netdb['key'])

    elif method == 'POST':
        resp = requests.post(url=url, headers=HEADERS, data=json, verify=False, cert=netdb['key'])

    elif method == 'PUT':
        resp = requests.put(url=url, headers=HEADERS, data=json, verify=False, cert=netdb['key'])

    elif method == 'DELETE':
        resp = requests.put(url=url, headers=HEADERS, data=json, verify=False, cert=netdb['key'])

    if resp.status_code in [200, 422]:
        return resp.json()
    else:
        return {
                'result': False,
                'error': True,
                'comment': f'netdb api error: {resp.status_code} {resp.reason}'
                }
