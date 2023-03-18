
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
    }


def load_yaml(path, column, outputter=None, display_progress=False):

    netdb_config = _get_netdb_config()
    url = netdb_config['url'] + column

    conf = yaml.safe_load(Path(path).read_text())

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    method = "POST"
    resp = salt.utils.http.query(
        url=url, method=method, header_dict=headers, data = json.dumps(conf)
    )

    if 'body' in resp:
        return json.loads(resp['body'])

    return resp


def get_column (column, device=None, outputter=None, display_progress=False):

    netdb_config = _get_netdb_config()
    url = netdb_config['url'] + column

    if device != None:
        url += '/' + device

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    method = "GET"
    resp = salt.utils.http.query(
        url=url, method=method, header_dict=headers
    )

    if 'body' in resp:
        return json.loads(resp['body'])

    return resp

