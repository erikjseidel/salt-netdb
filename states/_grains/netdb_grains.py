import salt.config
import salt.loader

__opts__ = salt.config.minion_config('/etc/salt/proxy')
__utils__ = salt.loader.utils(__opts__)

__virtualname__ = 'netdb_grains'
__proxyenabled__ = ['*']

def __virtual__():
    return __virtualname__

def netdb_grains():
    if 'netdb' in __pillar__:
        netdb = __pillar__['netdb']

        netdb_local = __pillar__.get('netdb_local')

        grains = __utils__['netdb.get_grains'](netdb, netdb_local)
        grains['id'] = netdb['id']

        return grains

    return {}
