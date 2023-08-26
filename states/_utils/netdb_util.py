import salt.utils.http
import json

HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        }

def __virtual__():
    netdb_config = __opts__["netdb"] if "netdb" in __opts__ else None

    if netdb_config:
        url = netdb_config.get("url", None)
        if not url:
            return ( False, 'netdb config not loaded' )
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

    if data:
        resp = salt.utils.http.query(
            url=url, method=method, header_dict=HEADERS, verify_ssl=False, data=json.dumps(data),
            cert = [ netdb['key'], netdb['key'] ]
        )
    else:
        resp = salt.utils.http.query(
            url=url, method=method, header_dict=HEADERS, verify_ssl=False,
            cert = [ netdb['key'], netdb['key'] ]
        )

    if 'body' in resp:
        return json.loads(resp['body'])
    else:
        return { 'result': False, 'error': True, 'comment': 'netdb util api error: ' +  resp['error'] }
