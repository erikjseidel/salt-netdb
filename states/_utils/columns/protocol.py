from typing import Literal, Dict, Optional, List
from ipaddress import IPv4Address, IPv4Network
from pydantic import Field
from ..base_types import BaseContainer, BaseColumnModel


class DHCPRange(BaseColumnModel):
    start_address: IPv4Address
    end_address: IPv4Address


class DHCPNetwork(BaseColumnModel):
    router_ip: IPv4Address
    network: IPv4Network
    ranges: List[DHCPRange]


class DHCPServer(BaseColumnModel):
    networks: List[DHCPNetwork]


class Services(BaseColumnModel):
    dhcp_server: Optional[DHCPServer] = None


class LLDP(BaseColumnModel):
    interfaces: Optional[List[str]] = None


class ISISInterface(BaseColumnModel):
    name: str
    passive: bool = False


class ISISRedistributeMap(BaseColumnModel):
    connected_map: Optional[str] = None
    static_map: Optional[str] = None


class ISISRedistributeLevel(BaseColumnModel):
    level_1: Optional[ISISRedistributeMap] = None
    level_2: Optional[ISISRedistributeMap] = None


class ISISRedistributePolicy(BaseColumnModel):
    ipv4: Optional[ISISRedistributeLevel] = None
    ipv6: Optional[ISISRedistributeLevel] = None


class ISIS(BaseColumnModel):
    level: int = Field(None, ge=1, le=3)
    lsp_mtu: int = Field(1471, ge=1200, le=9200)
    iso: str
    interfaces: List[ISISInterface]
    redistribute: Optional[ISISRedistributePolicy] = None


class Protocol(BaseColumnModel):
    isis: Optional[ISIS] = None
    lldp: Optional[LLDP] = None
    services: Optional[Services] = None


class ProtocolContainer(BaseContainer):
    __categories__ = ['services']

    column_type: Literal['protocol'] = 'protocol'
    column: Dict[str, Protocol]
