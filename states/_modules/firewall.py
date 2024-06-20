import logging

__virtualname__ = "firewall"

logger = logging.getLogger(__file__)

_COLUMN = 'firewall'


def __virtual__():
    return __virtualname__


def generate():
    """
    Generate dictionary for "state.apply firewall". This call takes no arguments.

    :return: a dictionary consisting of the following keys:

       * result: (bool) True state apply data is successully genarated; false otherwise.
       * error: (boot) True is state apply data generation fails. Not returned otherwise.
       * comment: (str) An explanation of the result

    CLI Example::

    .. code-block:: bash

        salt sin1 firewall.generate

    """

    return __utils__['column.pull'](_COLUMN)
