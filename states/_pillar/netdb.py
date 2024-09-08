from copy import deepcopy


def ext_pillar(*args, **kwargs):
    """
    Load netdb pillar from opts
    """

    pillar = {}
    if 'netdb' in __opts__:
        pillar['netdb'] = deepcopy(__opts__['netdb'])

    return pillar
