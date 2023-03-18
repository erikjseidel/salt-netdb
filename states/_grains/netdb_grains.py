import salt.config
import salt.loader

__opts__ = salt.config.minion_config('/etc/salt/proxy')
__utils__ = salt.loader.utils(__opts__)

__virtualname__ = 'netdb_grains'
__proxyenabled__ = ['*']

def __virtual__():
    return __virtualname__

def netdb_grains():
    pillar = __pillar__['netdb']

    grains = __utils__['netdb.get_grains'](pillar)
    grains['id'] = pillar['id']

    return grains
