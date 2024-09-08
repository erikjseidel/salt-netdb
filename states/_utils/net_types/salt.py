from pydantic import BaseModel

from net_types.netdb import ColumnObject


class SaltBaseReturn(BaseModel):
    result: bool = False
    comment: str = ''


class SaltColumnReturn(SaltBaseReturn):
    out: ColumnObject


class SaltDictReturn(SaltBaseReturn):
    out: dict


def salt_dict_return(**kwargs):
    """
    Shortcut wrapper for SaltDictReturn type
    """

    return SaltDictReturn(**kwargs).model_dump()
