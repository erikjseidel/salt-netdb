
from pathlib import Path
import yaml, json
import salt.utils.http


def load_yaml(path, column, outputter=None, display_progress=False):

    try:
        conf = yaml.safe_load(Path(path).read_text())
    except FileNotFoundError:
        return { 'result': False, 'error': True, 'comment': 'File not found.' }

    data = json.dumps(conf)

    return __utils__['netdb_runner.request'](column, data=data, method='POST')


def get_column (column, device=None, outputter=None, display_progress=False):

    return __utils__['netdb_runner.request'](column, method='GET')
