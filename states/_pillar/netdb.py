import copy


def ext_pillar(minion_id, pillar, *args, **kwargs):
    """
    Load netdb pillar from opts
    """

    pillar = {}
    if 'netdb' in __opts__:
        pillar['netdb'] = copy.deepcopy(__opts__['netdb'])

    return pillar
