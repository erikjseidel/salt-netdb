import salt.config
import salt.loader

__opts__ = salt.config.minion_config('/etc/salt/proxy')
__utils__ = salt.loader.utils(__opts__)

__virtualname__ = 'netdb_grains'
__proxyenabled__ = ['*']


def __virtual__():
    return __virtualname__


def netdb_grains() -> dict:
    """
    Load NetDB grains. Currently just overlays the device column onto the
    grains dict.
    """
    if 'netdb' in __pillar__:
        netdb_id = __pillar__['netdb']['id']

        grains = __utils__['netdb_api.get_api'](__pillar__).get_column(
            netdb_id, 'device'
        )
        grains['id'] = netdb_id

        return grains

    return {}
