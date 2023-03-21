# -*- coding: utf-8 -*-

import logging

__virtualname__ = "policy"

log = logging.getLogger(__file__)

_COLUMN = 'policy'

def __virtual__():
    return __virtualname__


def _netdb_pull():
    netdb_answer =  __salt__['netdb.get_column'](_COLUMN)

    if not netdb_answer['result'] or 'out' not in netdb_answer:
        netdb_answer.update({ 'error': True })

    return netdb_answer


def generate():
    """
    Generate dictionary for "state.apply policy". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1-proxy policy.generate

    """

    return _netdb_pull()
