
from pathlib import Path
import yaml, json
import salt.utils.http

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
        "url": __opts__["netdb"]["url"],
        "key": __opts__["netdb"]["key"],
    }


def _netdb_request(column, device=None, data=None, method="GET"):
    netdb = _get_netdb_config()

    if device:
        url = netdb['url'] + column + '/' + device
    else:
        url = netdb['url'] + column

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if data:
        resp = salt.utils.http.query(
            url=url, method=method, header_dict=headers, verify_ssl=False, data=data,
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


def load_yaml(path, column, outputter=None, display_progress=False):

    try:
        conf = yaml.safe_load(Path(path).read_text())
    except FileNotFoundError:
        return { 'result': False, 'error': True, 'comment': 'File not found.' }

    data = json.dumps(conf)

    return _netdb_request(column, data=data, method='POST')


def get_column (column, device=None, outputter=None, display_progress=False):

    return _netdb_request(column, method='GET')
