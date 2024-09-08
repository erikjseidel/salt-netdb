from typing import Literal, Optional, Dict, List
from ipaddress import IPv6Address, IPv4Address
from pydantic import ConfigDict, Field, IPvAnyAddress, IPvAnyNetwork
from ..base_types import BaseContainer, BaseColumnModel


class DeviceCVars(BaseColumnModel):
    ibgp_ipv4: Optional[IPv4Address] = None
    ibgp_ipv6: Optional[IPv6Address] = None
    iso: Optional[str] = None
    router_id: IPv4Address
    local_asn: int = Field(ge=1, lt=2**32)
    primary_ipv4: IPv4Address
    primary_ipv6: IPv6Address
    dns_servers: List[IPvAnyAddress]
    znsl_prefixes: List[IPvAnyNetwork]

    model_config = ConfigDict(extra='allow')


class Device(BaseColumnModel):
    location: str
    providers: List[str]
    roles: Optional[List[str]] = None
    node_name: str
    cvars: DeviceCVars


class DeviceContainer(BaseContainer):
    __flat__ = True

    column_type: Literal['device'] = 'device'
    column: Dict[str, Device]
