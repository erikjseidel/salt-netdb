#!jinja|yaml

{#

#}

znsl_ethernet:
  SIN1:
    bond0:
      description: Downstream LACP Bundle
      type: lacp
      lacp:
        hash_policy: layer3+4
        rate: fast
        min_links: 1
        members:
          - eth2
          - eth3
    bond0.15:
      address:
        "10.5.130.1/24":
          meta:
            role:
              - ipv4_address
              - znsl_private
      description: "ZNSL Private [NAT: MYREP2]"
      type: vlan
      vlan:
        id: 15
        parent: bond0
      policy:
        ipv4: MYREP2
    bond0.17:
      address: 
        "170.39.65.1/26":
          meta:
            role:
              - ipv4_address
              - znsl_public
          dns:
            ptr: sin1-rtr-vlan17.sin.as36198.net
        "2620:136:a001:17::1/64":
          meta:
            role:
              - ipv6_address
              - znsl_public
          dns:
            ptr: sin1-rtr-vlan17.sin.as36198.net
      description: ZNSL Public
      type: vlan
      vlan:
        id: 17
        parent: bond0
    bond0.88:
      address: 
        "192.168.88.10/24":
          meta:
            role:
              - ipv4_address
      description: Mikrotik Config LAN
      type: vlan
      vlan:
        id: 88
        parent: bond0
    bond0.902:
      address: 
        "170.39.65.65/29":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - management
            dns:
              ptr: sin1-rtr-vlan902.sin.as36198.net
      description: Management LAN
      type: vlan
      vlan:
        id: 902
        parent: bond0
   
  SIN2:
    eth1:
      address: 
        "23.181.64.68/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin2-sin3.l2ptp.as36198.net
        "2620:136:a009:af00::68/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin2-sin3.l2ptp.as36198.net
      type: ethernet
      description: SIN2-SIN3 L2 Link
      mtu: 1450
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

  SIN3:
    eth1:
      address: 
        "23.181.64.69/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin3-sin2.l2ptp.as36198.net
        "2620:136:a009:af00::69/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin3-sin2.l2ptp.as36198.net
      type: ethernet
      description: SIN3-SIN2 L2 Link
      mtu: 1450
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL
