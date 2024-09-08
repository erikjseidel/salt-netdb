from typing import Literal, Optional, Dict, List
from pydantic import Field, IPvAnyAddress, IPvAnyNetwork
from ..base_types import BaseContainer, BaseColumnModel


class PolicyBasicRule(BaseColumnModel):
    action: Literal['permit', 'deny']
    description: Optional[str] = None
    regex: str


class PolicyCommunityRule(PolicyBasicRule):
    pass


class PolicyCommunity(BaseColumnModel):
    description: Optional[str] = None
    rules: List[PolicyCommunityRule]


class PolicyASPathRule(PolicyBasicRule):
    pass


class PolicyASPath(BaseColumnModel):
    description: Optional[str] = None
    rules: List[PolicyASPathRule]


class PolicyRouteMapSet(BaseColumnModel):
    local_pref: Optional[int] = Field(None, ge=0, le=255)
    as_path_exclude: Optional[int] = Field(None, ge=1, lt=2**32)
    next_hop: Optional[IPvAnyAddress] = None
    origin: Optional[str] = None
    community: Optional[str] = None
    large_community: Optional[str] = None


class PolicyRouteMapMatch(BaseColumnModel):
    prefix_list: Optional[str] = None
    community_list: Optional[str] = None
    as_path: Optional[str] = None
    rpki: Literal['notfound', 'valid', 'invalid', None] = None


class PolicyRouteMapRule(BaseColumnModel):
    action: Literal['permit', 'deny']
    match: Optional[PolicyRouteMapMatch] = None
    set: Optional[PolicyRouteMapSet] = None
    number: int = Field(ge=0, le=999)
    continue_: Optional[int] = Field(None, ge=0, le=999, alias='continue')


class PolicyRouteMap(BaseColumnModel):
    rules: List[PolicyRouteMapRule]


class PolicyRouteMapBase(BaseColumnModel):
    ipv4: Optional[Dict[str, PolicyRouteMap]] = None
    ipv6: Optional[Dict[str, PolicyRouteMap]] = None


class PolicyPrefixListRules(BaseColumnModel):
    le: Optional[int] = Field(None, ge=0, le=128)
    ge: Optional[int] = Field(None, ge=0, le=128)
    prefix: IPvAnyNetwork


class PolicyPrefixList(BaseColumnModel):
    rules: List[PolicyPrefixListRules]


class PolicyPrefixListBase(BaseColumnModel):
    ipv4: Optional[Dict[str, PolicyPrefixList]] = None
    ipv6: Optional[Dict[str, PolicyPrefixList]] = None


class Policy(BaseColumnModel):
    prefix_lists: Optional[PolicyPrefixListBase] = None
    route_maps: Optional[PolicyRouteMapBase] = None
    aspath_lists: Optional[Dict[str, PolicyASPath]] = None
    community_lists: Optional[Dict[str, PolicyCommunity]] = None


class PolicyContainer(BaseContainer):
    __categories__ = [
        'prefix_lists',
        'route_maps',
        'aspath_lists',
        'community_lists',
    ]

    column_type: Literal['policy'] = 'policy'
    column: Dict[str, Policy]
