from typing import Literal, Optional, Dict, List
from ipaddress import IPv4Address
from pydantic import Field, IPvAnyAddress, IPvAnyNetwork
from ..base_types import BaseContainer, BaseColumnModel


class BGPOptions(BaseColumnModel):
    asn: int = Field(ge=1, lt=2**32)
    hold_time: Optional[int] = Field(None, ge=15, le=180)
    keepalive_time: Optional[int] = Field(None, ge=5, le=60)
    log_neighbor_changes: bool = False
    router_id: IPv4Address
    cluster_id: Optional[IPv4Address] = None


class BGPAddressFamilyElement(BaseColumnModel):
    networks: Optional[List[IPvAnyNetwork]] = None
    redistribute: List[str]


class BGPAddressFamily(BaseColumnModel):
    ipv4: Optional[BGPAddressFamilyElement] = None
    ipv6: Optional[BGPAddressFamilyElement] = None


class BGPRouteMap(BaseColumnModel):
    import_: Optional[str] = Field(None, alias='import')
    export: Optional[str] = None


class BGPFamilyOptions(BaseColumnModel):
    nhs: Optional[bool] = None
    max_prefixes: Optional[int] = Field(None, ge=1)
    route_reflector: Optional[bool] = None
    default_originate: Optional[bool] = None
    route_map: Optional[BGPRouteMap] = None


class BGPFamily(BaseColumnModel):
    ipv4: Optional[BGPFamilyOptions] = None
    ipv6: Optional[BGPFamilyOptions] = None


class BGPTimers(BaseColumnModel):
    holdtime: int = Field(ge=15, le=3000)
    keepalive: int = Field(ge=5, le=1000)


class BGPPeerGroup(BaseColumnModel):
    type: Literal['ibgp', 'ebgp'] = 'ebgp'
    source: Optional[IPvAnyAddress] = None
    family: Optional[BGPFamily] = None
    multihop: Optional[int] = Field(None, ge=1, le=255)
    password: Optional[str] = None
    remote_asn: Optional[int] = Field(None, ge=1, lt=2**32)


# Neighbor extends peergroup with a couple of additional options.
class BGPNeighbor(BGPPeerGroup):
    peer_group: Optional[str] = None
    timers: Optional[BGPTimers] = None
    reject_in: Optional[bool] = None
    reject_out: Optional[bool] = None


class BGP(BaseColumnModel):
    options: Optional[BGPOptions] = None
    address_family: Optional[BGPAddressFamily] = None
    peer_groups: Optional[Dict[str, BGPPeerGroup]] = None
    neighbors: Optional[Dict[IPvAnyAddress, BGPNeighbor]] = None


class BGPContainer(BaseContainer):
    __categories__ = ['peer_groups', 'neighbors']

    column_type: Literal['bgp'] = 'bgp'
    column: Dict[str, BGP]
