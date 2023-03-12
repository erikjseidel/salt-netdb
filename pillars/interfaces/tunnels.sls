#!jinja|yaml

{#

#}

znsl_tunnels:
  SIN1:
    tun370:
      address:
        "23.181.64.71/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep1-sin2.ipv4.ptp.as36198.net
        "2620:136:a009:af00::71/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep1-sin2.ipv6.ptp.as36198.net
      type: gre
      description: SIN1-SIN2 L3 Link MYREP1
      mtu: 1450
      ttl: 255
      remote: 139.180.130.102
      source: 101.100.165.107
      interface: eth0

    tun372:
      address:
        "23.181.64.73/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep2-sin2.ipv4.ptp.as36198.net
        "2620:136:a009:af00::73/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep2-sin2.ipv6.ptp.as36198.net
      type: gre
      description: SIN1-SIN2 L3 Link MYREP2
      mtu: 1450
      ttl: 255
      remote: 139.180.130.102
      source: 101.100.165.109
      interface: eth1

    tun374:
      address:
        "23.181.64.75/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep1-sin3.ipv4.ptp.as36198.net
        "2620:136:a009:af00::75/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep1-sin3.ipv6.ptp.as36198.net
      type: gre
      description: SIN1-SIN3 L3 Link MYREP1
      mtu: 1450
      ttl: 255
      remote: 66.42.59.36
      source: 101.100.165.107
      interface: eth0

    tun376:
      address:
        "23.181.64.77/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep2-sin3.ipv4.ptp.as36198.net
        "2620:136:a009:af00::77/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep2-sin3.ipv6.ptp.as36198.net
      type: gre
      description: SIN1-SIN3 L3 Link MYREP2
      mtu: 1450
      ttl: 255
      remote: 66.42.59.36
      source: 101.100.165.109
      interface: eth1

    tun378:
      address:
        "23.181.64.79/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep1-aus4.ipv4.ptp.as36198.net
        "2620:136:a009:af00::79/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep1-aus4.ipv6.ptp.as36198.net
      type: gre
      description: SIN1-AUS4 L3 Link MYREP1
      mtu: 1450
      ttl: 255
      remote: 71.78.15.27
      source: 101.100.165.107
      interface: eth0

    tun380:
      address:
        "23.181.64.81/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep2-aus4.ipv4.ptp.as36198.net
        "2620:136:a009:af00::81/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin1-myrep2-aus4.ipv6.ptp.as36198.net
      type: gre
      description: SIN1-AUS4 L3 Link MYREP2
      mtu: 1450
      ttl: 255
      remote: 71.78.15.27
      source: 101.100.165.109
      interface: eth1

  SIN2:
    tun202:
      address:
        "23.181.64.2/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin2-fra1.l2ptp.as36198.net
        "2620:136:a009:af00::2/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin2-fra1.l2ptp.as36198.net
      type: l2gre
      description: SIN2-FRA1 L2 Link
      mtu: 1450
      ttl: 255
      remote: 194.50.19.126
      source: 139.180.130.102
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun261:
      address:
        "23.181.64.61/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin2-dfw4.l2ptp.as36198.net
        "2620:136:a009:af00::61/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin2-dfw4.l2ptp.as36198.net
      type: l2gre
      description: SIN2-DFW4 L2 Link
      mtu: 1450
      ttl: 255
      remote: 142.202.220.102
      source: 139.180.130.102
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun263:
      address:
        "23.181.64.63/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin2-dfw2.l2ptp.as36198.net
        "2620:136:a009:af00::63/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin2-dfw2.l2ptp.as36198.net
      type: l2gre
      description: SIN2-DFW2 L2 Link
      mtu: 1450
      ttl: 255
      remote: 155.138.243.160
      source: 139.180.130.102
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun370:
      address:
        "23.181.64.70/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin2-sin1-myrep1.ipv4.ptp.as36198.net
        "2620:136:a009:af00::70/127":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin2-sin1-myrep1.ipv4.ptp.as36198.net
      type: gre
      description: SIN2-SIN1 L3 Link MYREP1
      mtu: 1450
      ttl: 255
      remote: 101.100.165.107
      source: 139.180.130.102
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun372:
      address:
        "23.181.64.72/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin2-sin1-myrep2.ipv4.ptp.as36198.net
        "2620:136:a009:af00::72/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin2-sin1-myrep2.ipv6.ptp.as36198.net
      type: gre
      description: SIN2-SIN1 L3 Link MYREP2
      mtu: 1450
      ttl: 255
      remote: 101.100.165.109
      source: 139.180.130.102
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

  SIN3:
    tun204:
      address:
        "23.181.64.4/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin3-fra1.l2ptp.as36198.net
        "2620:136:a009:af00::4/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin3-fra1.l2ptp.as36198.net
      type: l2gre
      description: SIN3-FRA1 L2 Link
      mtu: 1450
      ttl: 255
      remote: 194.50.19.126
      source: 66.42.59.36
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun264:
      address:
        "23.181.64.65/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin3-dfw4.l2ptp.as36198.net
        "2620:136:a009:af00::65/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin3-dfw4.l2ptp.as36198.net
      type: l2gre
      description: SIN3-DFW4 L2 Link
      mtu: 1450
      ttl: 255
      remote: 142.202.220.102
      source: 66.42.59.36
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun266:
      address:
        "23.181.64.67/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin3-dfw3.l2ptp.as36198.net
        "2620:136:a009:af00::67/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: sin3-dfw3.l2ptp.as36198.net
      type: l2gre
      description: SIN3-DFW3 L2 Link
      mtu: 1450
      ttl: 255
      remote: 144.202.72.168
      source: 66.42.59.36
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun374:
      address:
        "23.181.64.74/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin3-sin1-myrep1.ipv4.ptp.as36198.net
        "2620:136:a009:af00::74/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin3-sin1-myrep1.ipv6.ptp.as36198.net
      type: gre
      description: SIN3-SIN1 L3 Link MYREP1
      mtu: 1450
      ttl: 255
      remote: 101.100.165.107
      source: 66.42.59.36
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun376:
      address:
        "23.181.64.76/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin3-sin1-myrep2.ipv4.ptp.as36198.net
        "2620:136:a009:af00::76/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l3ptp
            dns:
              ptr: sin3-sin1-myrep2.ipv6.ptp.as36198.net
      type: gre
      description: SIN3-SIN1 L3 Link MYREP2
      mtu: 1450
      ttl: 255
      remote: 101.100.165.109
      source: 66.42.59.36
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

  FRA1:
    tun40:
      address:
        "23.181.64.41/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: fra1-dfw4.l2ptp.as36198.net
        "2620:136:a009:af00::41/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: fra1-dfw4.l2ptp.as36198.net
      type: l2gre
      description: FRA1-DFW4 L2 Link
      mtu: 1450
      ttl: 255
      remote: 142.202.220.102
      source: 194.50.19.126
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun46:
      address:
        "23.181.64.47/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: fra1-dfw3.l2ptp.as36198.net
        "2620:136:a009:af00::47/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: fra1-dfw3.l2ptp.as36198.net
      type: l2gre
      description: FRA1-DFW3 L2 Link
      mtu: 1450
      ttl: 255
      key: 23.181.64.46
      remote: 144.202.72.168
      source: 194.50.19.126
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun203:
      address:
        "23.181.64.3/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: fra1-sin2.l2ptp.as36198.net
        "2620:136:a009:af00::3/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: fra1-sin2.l2ptp.as36198.net
      type: l2gre
      description: FRA1-SIN2 L2 Link
      mtu: 1450
      ttl: 255
      remote: 139.180.130.102
      source: 194.50.19.126
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL

    tun205:
      address:
        "23.181.64.5/31":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - l2ptp
            dns:
              ptr: fra1-sin3.l2ptp.as36198.net
        "2620:136:a009:af00::5/127":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - l2ptp
            dns:
              ptr: fra1-sin3.l2ptp.as36198.net
      type: l2gre
      description: FRA1-SIN3 L2 Link
      mtu: 1450
      ttl: 255
      remote: 66.42.59.36
      source: 194.50.19.126
      firewall:
        local:
          ipv4: INTERNAL-LOCAL
          ipv6: 6-INTERNAL-LOCAL
