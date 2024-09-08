from typing import Annotated, Union, Literal, Optional
from pydantic import BaseModel, HttpUrl, Field

from .base_types import FamilyType
from .columns.device import DeviceContainer
from .columns.firewall import FirewallContainer
from .columns.policy import PolicyContainer
from .columns.interface import InterfaceContainer
from .columns.bgp import BGPContainer
from .columns.protocol import ProtocolContainer

COLUMN_FACTORY = {
    'device': DeviceContainer,
    'firewall': FirewallContainer,
    'policy': PolicyContainer,
    'interface': InterfaceContainer,
    'bgp': BGPContainer,
    'protocol': ProtocolContainer,
}

COLUMN_TYPES = list(COLUMN_FACTORY.keys())

COLUMN_CLASSES = list(COLUMN_FACTORY.values())

ColumnType = Annotated[str, Literal[*COLUMN_TYPES]]

ColumnObject = Annotated[Union[*COLUMN_CLASSES], Field(discriminator='column_type')]


class Override(BaseModel):
    """
    Abstract type used to derive NetdbDocument and OverrideDocument
    types

    """

    column_type: ColumnType
    set_id: str
    category: Optional[str] = None
    family: Optional[FamilyType] = None
    element_id: Optional[str] = None
    data: dict


class SaltBaseReturn(BaseModel):
    result: bool = True
    error: bool = False
    comment: str


class SaltColumnReturn(SaltBaseReturn):
    out: ColumnObject


class SaltDictReturn(SaltBaseReturn):
    out: dict


class NetdbPillar(BaseModel):
    id: str
    url: HttpUrl
    util_url: Optional[HttpUrl] = None


class NetdbLocalPillar(BaseModel):
    enabled: str
    url: HttpUrl
