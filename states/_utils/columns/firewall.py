from typing import Literal, Optional, Dict, List
from pydantic import Field, IPvAnyInterface
from ..base_types import BaseContainer, BaseColumnModel


class FirewallOptions(BaseColumnModel):
    all_ping: Optional[str] = Field(None, alias='all-ping')
    broadcast_ping: Optional[str] = Field(None, alias='broadcast-ping')
    config_trap: Optional[str] = Field(None, alias='config-trap')
    ipv6_receive_redirects: Optional[str] = Field(None, alias='ipv6-receive-redirects')
    ipv6_src_route: Optional[str] = Field(None, alias='ipv6-src-route')
    log_martians: Optional[str] = Field(None, alias='log-martians')
    send_redirects: Optional[str] = Field(None, alias='send-redirects')
    source_validation: Optional[str] = Field(None, alias='source-validation')
    syn_cookies: Optional[str] = Field(None, alias='syn-cookies')
    twa_hazards_protection: Optional[str] = Field(None, alias='twa-hazards-protection')
    ip_src_route: Optional[str] = Field(None, alias='ip-src-route')
    receive_redirects: Optional[str] = Field(None, alias='receive-redirects')


class FirewallMSSClamp(BaseColumnModel):
    ipv4: int = Field(ge=556, le=9172)
    ipv6: int = Field(ge=1280, le=9172)
    interfaces: List[str]


class FirewallStatePolicy(BaseColumnModel):
    established: Literal['accept', 'drop']
    related: Literal['accept', 'drop']


class FirewallZoneRule(BaseColumnModel):
    ipv4_ruleset: Optional[str] = None
    ipv6_ruleset: Optional[str] = None
    zone: str


class FirewallZonePolicy(BaseColumnModel):
    from_: Optional[List[FirewallZoneRule]] = Field(None, alias='from')
    interfaces: Optional[List[str]] = None
    default_action: Literal['accept', 'drop']


class FirewallGroup(BaseColumnModel):
    type: Literal['network']
    networks: List[IPvAnyInterface]


class FirewallGroupBase(BaseColumnModel):
    ipv4: Optional[Dict[str, FirewallGroup]] = None
    ipv6: Optional[Dict[str, FirewallGroup]] = None


class FirewallPolicyInterfaces(BaseColumnModel):
    ingress: Optional[str] = None
    egress: Optional[str] = None


class FirewallPolicyTarget(BaseColumnModel):
    network_group: Optional[str] = None
    port: Optional[List[int]] = None


class FirewallPolicyRule(BaseColumnModel):
    action: Literal['accept', 'drop', 'jump']
    state: Optional[List[Literal['established', 'related']]] = None
    source: Optional[FirewallPolicyTarget] = None
    destination: Optional[FirewallPolicyTarget] = None
    protocol: Optional[str] = None

    # Vyos 1.4
    policy: Optional[str] = None
    interfaces: Optional[FirewallPolicyInterfaces] = None


class FirewallPolicy(BaseColumnModel):
    default_action: Literal['accept', 'drop']
    rules: Optional[List[FirewallPolicyRule]] = None


class FirewallPolicyBase(BaseColumnModel):
    ipv4: Optional[Dict[str, FirewallPolicy]] = None
    ipv6: Optional[Dict[str, FirewallPolicy]] = None


class Firewall(BaseColumnModel):
    policies: Optional[FirewallPolicyBase] = None
    groups: Optional[FirewallGroupBase] = None
    state_policy: Optional[FirewallStatePolicy] = None
    mss_clamp: Optional[FirewallMSSClamp] = None
    zone_policy: Optional[Dict[str, FirewallZonePolicy]] = None
    options: Optional[FirewallOptions] = None

    # Vyos 1.4
    policy_base: Optional[FirewallPolicyBase] = None


class FirewallContainer(BaseContainer):
    __categories__ = [
        'policies',
        'groups',
        'zone_policy',
    ]

    column_type: Literal['firewall'] = 'firewall'
    column: Dict[str, Firewall]
