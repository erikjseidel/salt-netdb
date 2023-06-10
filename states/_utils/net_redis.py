import logging, json, redis

logger = logging.getLogger(__file__)

# For docker
_NET_REDIS_HOST = '172.17.0.1'
_NET_REDIS_PORT = 6379
_NET_REDIS_DB   = '0'

def _get_redis_server():
    return redis.Redis(
            host=_NET_REDIS_HOST, 
            port=_NET_REDIS_PORT, 
            db=_NET_REDIS_DB
            )


def get_kv( redis_key ):

    _redis_server = _get_redis_server()

    if _redis_server is None:
        return { 'return': False, 'out': None }

    value = _redis_server.get(redis_key)
    if not value:
        return { 'return': True, 'out': None }

    out_data = json.loads(value)

    return { 'return': True, 'out': out_data }


def set_kv( redis_key, value ):

    _redis_server = _get_redis_server()

    if _redis_server is None:
        return { 'return': False, 'out': None }

    _redis_server.set(redis_key, json.dumps(value))
