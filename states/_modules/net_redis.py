import logging, json

logger = logging.getLogger(__file__)

__virtualname__ = 'net_redis'


"""

Entry lists are lists of strings identified by REDIS keys and further divided by router identified
by grains.id. An entry list is thus organized as follows:

key:
    - ROUTER_ID_A:
        - str1
        - str2
        - etc
    - ROUTER_ID_B:
        - str1
        - etc
    etc.

Division by router id allows for multiple proxy minions to share the same redis database / host.

If the entry list (i.e. key) does not exist, it will be added by add_entry. If an router id is not
found in an entry list (i.e. key) it will be added by add_entry. The is the case for when no list
is found for a router. Once added keys, routers, lists will not be deleted (e.g. if all entries for
a router are removed, the empty list and router id key will remain in place).

"""


def add_entry(key, entry):
    """
    Adds an entry from list of salt managed entries for router grains.id by key

    :param key: name of the entry list to query
    :param entry: the entry to be added
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if entry removed; false otherwise
       * comment: (str) An explanation of the result
       * out: (str[]) the new entry list

    """
    router = __grains__['id']

    entries = __utils__['net_redis.get_kv'](key)

    if entries['out'] == None:
        entries['out'] = {router: [entry]}

    else:
        if router in entries['out'] and isinstance(entries['out'][router], list):
            if entry in entries['out'][router]:
                return {
                    'return': False,
                    'comment': 'Entry already added in REDIS',
                    'out': '',
                }
            else:
                entries['out'][router].append(entry)
        else:
            entries['out'][router] = [entry]

    __utils__['net_redis.set_kv'](key, entries['out'])

    return {
        "result": True,
        "comment": 'Entry successfully added',
        'out': entries['out'][router],
    }


def remove_entry(key, entry):
    """
    Removes an entry from list of salt managed entries for router grains.id by key

    :param key: name of the entry list to query
    :param entry: the entry to be removed
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if entry removed; false otherwise
       * comment: (str) An explanation of the result
       * out: (str[]) the new entry list

    """
    router = __grains__['id']

    already_exists = False

    entries = __utils__['net_redis.get_kv'](key)

    if entries['out'] != None:
        if router in entries['out']:
            if entry in entries['out'][router]:
                already_exists = True

    if already_exists:
        entries['out'][router].remove(entry)

        __utils__['net_redis.set_kv'](key, entries['out'])

        return {
            "result": True,
            "comment": 'Entry removed',
            'out': entries['out'][router],
        }

    return {"result": False, "comment": "Entry not found"}


def get_entries(key):
    """
    Return a list of entries for router grains.id by REDIS key.

    :param key: name of the entry list to query
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if router has entries for key `key'; false otherwise
       * comment: (str) (only if return: False) an explanation

    """
    router = __grains__['id']
    entries = __utils__['net_redis.get_kv'](key)

    if entries['out'] != None:
        if router in entries['out'].keys():
            return {'return': True, 'out': entries['out'][router]}

    return {'return': False, 'comment': 'No entries found', 'out': []}


def check_entry(key, entry):
    """
    Check if an entry exists and an entry list stored in `key' for router grains.id

    :param key: name of the entry list to query
    :param entry: name of the entry to query
    :return: a dictionary consisting of the following keys:

       * result: (bool) True is query succeeds; false otherwise
       * comment: (str) (only if return: False) an explanation
       * out: True is router grains.id has this entry; otherwise false

    """

    entries = get_entries(key)['out']

    if entry in entries:
        ret = {"result": True, "comment": "Entry found", 'out': True}
    else:
        ret = {"result": True, "comment": "Entry not found", 'out': False}

    return ret
