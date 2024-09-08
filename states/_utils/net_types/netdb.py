from typing import Annotated, Union, Literal, Optional
from pydantic import BaseModel, Field

from net_types.base import FamilyType

from net_types.columns.device import DeviceContainer
from net_types.columns.firewall import FirewallContainer
from net_types.columns.policy import PolicyContainer
from net_types.columns.interface import InterfaceContainer
from net_types.columns.bgp import BGPContainer
from net_types.columns.protocol import ProtocolContainer

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

ColumnObject = Annotated[Union[*COLUMN_CLASSES], Field(discriminator='column_type')]  # type: ignore


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
