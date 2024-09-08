from typing import Literal, Optional, Dict, List
from ipaddress import IPv4Address
from pydantic import RootModel, Field, IPvAnyInterface, IPvAnyAddress
from ..base_types import BaseContainer, BaseColumnModel


class InterfaceAddress(BaseColumnModel):
    meta: dict


class InterfaceVLANOptions(BaseColumnModel):
    id: int = Field(ge=1, le=4096)
    parent: str


class InterfaceLACPOptions(BaseColumnModel):
    hash_policy: Literal['layer2+3', 'layer3+4']
    rate: Literal['fast', 'slow']
    min_links: int = Field(ge=1, le=5)
    members: List[str]


class InterfacePolicy(BaseColumnModel):
    ipv4: Optional[str] = None
    ipv6: Optional[str] = None


class InterfaceFirewall(BaseColumnModel):
    local: Optional[InterfacePolicy] = None
    egress: Optional[InterfacePolicy] = None
    ingress: Optional[InterfacePolicy] = None


class Interface(BaseColumnModel):
    type: Literal['ethernet', 'vlan', 'lacp', 'dummy', 'gre', 'l2gre']
    disabled: bool = False
    offload: bool = False
    use_dhcp: bool = False
    ipv6_autoconf: bool = False
    description: Optional[str] = None
    interface: Optional[str] = None
    mac_address: Optional[str] = None
    vrf: Optional[str] = None
    mtu: Optional[int] = Field(None, ge=1280, le=9192)
    ttl: Optional[int] = Field(None, ge=1, le=255)
    key: Optional[IPv4Address] = None
    remote: Optional[IPvAnyAddress] = None
    source: Optional[IPvAnyAddress] = None
    address: Optional[Dict[IPvAnyInterface, InterfaceAddress]] = None
    vlan: Optional[InterfaceVLANOptions] = None
    lacp: Optional[InterfaceLACPOptions] = None
    firewall: Optional[InterfaceFirewall] = None
    policy: Optional[InterfacePolicy] = None


class InterfaceRoot(RootModel):
    root: Dict[str, Interface]


class InterfaceContainer(BaseContainer):
    column_type: Literal['interface'] = 'interface'
    column: Dict[str, InterfaceRoot]
