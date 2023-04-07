
import salt.utils.http
import json

_HEADERS = {
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


def request(column, device=None, data=None, test=False, method="GET"):
    netdb = _get_netdb_config()

    if test:
        url = netdb['url'] + column + '/validate'
    elif device:
        url = netdb['url'] + column + '/' + device
    else:
        url = netdb['url'] + column

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if data:
        resp = salt.utils.http.query(
            url=url, method=method, header_dict=headers, verify_ssl=False, data=json.dumps(data),
            cert = [ netdb['key'], netdb['key'] ]
        )
    else:
        resp = salt.utils.http.query(
            url=url, method=method, header_dict=headers, verify_ssl=False,
            cert = [ netdb['key'], netdb['key'] ]
        )

    if 'body' in resp:
        return json.loads(resp['body'])
    else:
        return { 'result': False, 'error': True, 'comment': 'netdb api error: ' +  resp['error'] }


def _alter(column, data, method='GET', test=True):
    netdb_answer = request(column, data = data, test=test,  method=method)

    # no configuration to be validated for delete method.
    if method == 'DELETE' and test:
        return { 'result': False, 'comment': 'Test run. Database not updated.', 'out': data }

    if netdb_answer['result']:
        netdb_answer.update({'out': data})

    return netdb_answer


def get(column, device=None, data=None):
    return request(column, device, data, method="GET")


def save(column, data, test=True):
    return _alter(column, data=data, method='POST', test=test)


def update(column, data, test=True):
    return _alter(column, data=data, method='PUT', test=test)


def delete(column, data, test=True):
    return _alter(column, data=data, method='DELETE', test=test)


def call_netdb_util(endpoint, data=None, method='GET'):
    netdb = _get_netdb_config()

    url = netdb['util_url'] + endpoint

    if data:
        resp = salt.utils.http.query(
            url=url, method=method, header_dict=_HEADERS, verify_ssl=False, data=json.dumps(data),
            cert = [ netdb['key'], netdb['key'] ]
        )
    else:
        resp = salt.utils.http.query(
            url=url, method=method, header_dict=_HEADERS, verify_ssl=False,
            cert = [ netdb['key'], netdb['key'] ]
        )

    if 'body' in resp:
        return json.loads(resp['body'])
    else:
        return { 'result': False, 'error': True, 'comment': 'netdb util api error: ' +  resp['error'] }
