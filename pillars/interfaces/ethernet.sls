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

  AUS4:
    eth6.66:
      address:
        "170.39.66.62/26":
          meta:
            role:
              - ipv4_address
              - znsl_private
              - magic_transit
          dns:
            ptr: aus4-rtr-vlan66.aus.as36198.net
      description: "Magic Transit LAN"
      type: vlan
      vlan:
        id: 66
        parent: eth6
    eth6.717:
      address:
        "170.39.64.126/25":
          meta:
            role:
              - ipv4_address
              - znsl_public
          dns:
            ptr: aus4-rtr-vlan717.aus.as36198.net
        "2620:136:a009:17::1/64":
          meta:
            role:
              - ipv6_address
              - znsl_public
      description: "ZNSL Main LAN"
      type: vlan
      vlan:
        id: 717
        parent: eth6
    eth6.902:
      address:
        "170.39.64.225/28":
          meta:
            role:
              - ipv4_address
              - znsl_public
          dns:
            ptr: aus4-rtr-vlan902.aus.as36198.net
      description: ZNSL Management
      type: vlan
      vlan:
        id: 902
        parent: eth6

  DFW2:
    eth1:
      address: 
        "23.181.64.48/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw2-dfw3.l2ptp.as36198.net
        "2620:136:a009:af00::48/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw2-dfw3.l2ptp.as36198.net
      type: ethernet
      description: DFW2-DFW3 L2 Link
      mtu: 1450
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

  DFW3:
    eth1:
      address: 
        "23.181.64.49/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw3-dfw2.l2ptp.as36198.net
        "2620:136:a009:af00::49/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw3-dfw2.l2ptp.as36198.net
      type: ethernet
      description: DFW3-DFW2 L2 Link
      mtu: 1450
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

  DFW4:
    eth3:
      address: 
        "23.181.64.129/29":
          meta:
            role:
              - ipv4_address
              - znsl_public
            dns:
              ptr: dfw-public-lan.rtr-dfw4.dfw.as36198.net
        "2620:136:a008:7517::1/64":
          meta:
            role:
              - ipv6_address
              - znsl_public
            dns:
              ptr: dfw-public-lan.rtr-dfw4.dfw.as36198.net
      type: ethernet
      description: Internal Network
      mtu: 1450
      offload: y
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth4:
      address: 
        "170.39.66.129/28":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - magic_transit
            dns:
              ptr: dfw-magic-lan.rtr-dfw4.dfw.as36198.net
      type: ethernet
      description: Magic Transit DFW
      mtu: 1450
      offload: y
      firewall:
        local:
          ipv4: INTERNAL-LOCAL

    eth5:
      address: 
        "23.181.64.32/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-dfw3.l2ptp.as36198.net
        "2620:136:a009:af00::32/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-dfw3.l2ptp.as36198.net
      type: ethernet
      description: DFW4-DFW3 L2 Link
      mtu: 1450
      offload: y
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth6:
      address: 
        "23.181.64.34/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-dfw2.l2ptp.as36198.net
        "2620:136:a009:af00::34/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-dfw2.l2ptp.as36198.net
      type: ethernet
      description: DFW4-DFW2 L2 Link
      mtu: 1450
      offload: y
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth7:
      address: 
        "23.181.64.36/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-mci2.l2ptp.as36198.net
        "2620:136:a009:af00::36/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-mci2.l2ptp.as36198.net
      type: ethernet
      description: DFW4-MCI2 L2 Link
      mtu: 1450
      offload: y
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth8:
      address: 
        "23.181.64.38/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-mci3.l2ptp.as36198.net
        "2620:136:a009:af00::38/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-mci3.l2ptp.as36198.net
      type: ethernet
      description: DFW4-MCI3 L2 Link
      mtu: 1450
      offload: y
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth9:
      address: 
        "23.181.64.40/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-fra1.l2ptp.as36198.net
        "2620:136:a009:af00::40/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-fra1.l2ptp.as36198.net
      type: ethernet
      description: DFW4-FRA1 L2 Link
      mtu: 1450
      offload: y
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth10:
      address: 
        "23.181.64.60/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-sin2.l2ptp.as36198.net
        "2620:136:a009:af00::60/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-sin2.l2ptp.as36198.net
      type: ethernet
      description: DFW4-SIN2 L2 Link
      mtu: 1450
      offload: y
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth11:
      address: 
        "23.181.64.64/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-sin3.l2ptp.as36198.net
        "2620:136:a009:af00::64/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: dfw4-sin3.l2ptp.as36198.net
      type: ethernet
      description: DFW4-SIN3 L2 Link
      mtu: 1450
      offload: y
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

  MCI2:
    eth2:
      address: 
        "23.181.64.37/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci2-dfw4.l2ptp.as36198.net
        "2620:136:a009:af00::37/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci2-dfw4.l2ptp.as36198.net
      type: ethernet
      description: MCI2-DFW4 L2 Link
      mtu: 1450
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth4:
      address: 
        "23.181.64.50/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci2-mci3.l2ptp.as36198.net
        "2620:136:a009:af00::50/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci2-mci3.l2ptp.as36198.net
      type: ethernet
      description: MCI2-MCI3 L2 Link
      mtu: 1450
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth5:
      address: 
        "23.181.64.42/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci2-dfw2.l2ptp.as36198.net
        "2620:136:a009:af00::42/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci2-dfw2.l2ptp.as36198.net
      type: ethernet
      description: MCI2-DFW2 L2 Link
      mtu: 1450
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth6:
      address: 
        "23.181.64.44/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci2-dfw3.l2ptp.as36198.net
        "2620:136:a009:af00::44/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci2-dfw3.l2ptp.as36198.net
      type: ethernet
      description: MCI2-DFW3 L2 Link
      mtu: 1450
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

  MCI3:
    eth2:
      address: 
        "23.181.64.39/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci3-dfw4.l2ptp.as36198.net
        "2620:136:a009:af00::39/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci3-dfw4.l2ptp.as36198.net
      type: ethernet
      description: MCI3-DFW4 L2 Link
      mtu: 1450
      offload: n
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    eth3:
      address: 
        "23.181.64.51/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci3-mci2.l2ptp.as36198.net
        "2620:136:a009:af00::51/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: mci3-mci2.l2ptp.as36198.net
      type: ethernet
      description: MCI3-MCI2 L2 Link
      mtu: 1450
      offload: n
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL
