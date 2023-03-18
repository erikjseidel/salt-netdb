
import salt.utils.http
import json

def get_grains(pillar):
    router = pillar['id'].upper()

    url = pillar['url'] + 'device' + '/' + router

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    method = "GET"
    resp = salt.utils.http.query(
        url=url, method=method, header_dict=headers
    )

    if 'body' in resp:
        return json.loads(resp['body'])['out'][router]
    else:
        return {}
