import logging
from netdb_util_api import NetdbUtilAPI

__virtualname__ = "cfdns"

_ENDPOINT = 'connectors/cfdns/{}'

logger = logging.getLogger(__file__)


def __virtual__():
    return __virtualname__


def synchronize(test=True):
    """
    Request update for netdb-util managed Cloudflare PTR zones.

    :param test: Perform the update if false, only list update actions if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if update / list IPs successful; false otherwise
       * out: a list of netdb managed PTRs in CF zones, relevent attributes and
              action required.

    ptr['action'] values are:
       * create: PTR does not exist in CF zone. Record will be created
       * update: PTR exists but does not match netdb record; will be updated
       * delete: PTR in CF zone does not exist in netdb; will be deleted
       * pass:   CF and netdb records align. No action required.

    CLI Example::

    .. code-block:: bash

        salt-run cfdns.synchronize test=False

    """

    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    return NetdbUtilAPI(__salt__['pillar.show_pillar']()).post(
        _ENDPOINT.format('update'), test=test
    )


def get_ptrs():
    """
    Return CF managed zones and PTR records.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if fetch successful; false otherwise
       * out: a dict of CF managed zones and PTR records and relevent attributes.

    CLI Example::

    .. code-block:: bash

        salt-run cfdns.get_ptrs

    """
    return NetdbUtilAPI(__salt__['pillar.show_pillar']()).get(
        _ENDPOINT.format('records')
    )


def get_zones():
    """
    Return CF managed zones.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True if fetch successful; false otherwise
       * out: a dict of CF managed zones.

    CLI Example::

    .. code-block:: bash

        salt-run cfdns.get_zones

    """
    return NetdbUtilAPI(__salt__['pillar.show_pillar']()).get(_ENDPOINT.format('zones'))


def upsert_zone(prefix, account, zone, managed, test=True):
    """
    Request addition / update of a CF managed zone identified by CIDR

    :param prefix:  Reverse DNS zone identified by CIDR
    :param account: Cloudflare account ID
    :param zone:    Cloudflare zone ID
    :param managed: If true any records in zone not matched by netdb will be deleted.
    :param test:    Perform the update if false, only list update actions if true.
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if update / list IPs successful; false otherwise
       * out: a list of netdb managed PTRs in CF zones, relevent attributes and
              action required.

    CLI Example::

    .. code-block:: bash

        salt-run cfdns.upsert_zone 23.181.64.0/24 847e539c1cd80 224c1ba9e358 managed=True

    """
    if not isinstance(test, bool):
        return {"result": False, "comment": "test only accepts true or false."}

    if not isinstance(managed, bool):
        return {"result": False, "comment": "managed accepts true or false."}

    data = {
        "prefix": prefix,
        "zone": zone,
        "account": account,
        "managed": managed,
    }

    return NetdbUtilAPI(__salt__['pillar.show_pillar']()).post(
        _ENDPOINT.format('zones'), data=data, test=test
    )


def delete_zone(prefix):
    """
    Request deletion of a CF managed zone identified by CIDR

    :param prefix:  Reverse DNS zone identified by CIDR
    :return: a dictionary consisting of the following keys:

       * result: (bool) True if delete action successful; false otherwise

    CLI Example::

    .. code-block:: bash

        salt-run cfdns.delete_zone 23.181.64.0/24

    """
    params = {'prefix': prefix}

    return NetdbUtilAPI(__salt__['pillar.show_pillar']()).delete(
        _ENDPOINT.format('zones'), params=params
    )
