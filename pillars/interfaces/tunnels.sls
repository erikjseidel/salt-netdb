#!jinja|yaml

{#

#}

{%- set node = pillar.node %}
znsl_tunnels:
  SIN1:
    tun370:
      ipv4_address: 23.181.64.71/31
      ipv6_address: 2620:136:a009:af00::71/127
      type: gre
      description: SIN1-SIN2 L3 Link MYREP1
      mtu: 1450
      ttl: 255
      remote: 139.180.130.102
      source: 101.100.165.107
      interface: eth0

    tun372:
      ipv4_address: 23.181.64.73/31
      ipv6_address: 2620:136:a009:af00::73/127
      type: gre
      description: SIN1-SIN2 L3 Link MYREP2
      mtu: 1450
      ttl: 255
      remote: 139.180.130.102
      source: 101.100.165.109
      interface: eth1

    tun374:
      ipv4_address: 23.181.64.75/31
      ipv6_address: 2620:136:a009:af00::75/127
      type: gre
      description: SIN1-SIN3 L3 Link MYREP1
      mtu: 1450
      ttl: 255
      remote: 66.42.59.36
      source: 101.100.165.107
      interface: eth0

    tun376:
      ipv4_address: 23.181.64.77/31
      ipv6_address: 2620:136:a009:af00::77/127
      type: gre
      description: SIN1-SIN3 L3 Link MYREP2
      mtu: 1450
      ttl: 255
      remote: 66.42.59.36
      source: 101.100.165.109
      interface: eth1

    tun378:
      ipv4_address: 23.181.64.79/31
      ipv6_address: 2620:136:a009:af00::79/127
      type: gre
      description: SIN1-AUS4 L3 Link MYREP1
      mtu: 1450
      ttl: 255
      remote: 71.78.15.27
      source: 101.100.165.107
      interface: eth0

    tun380:
      ipv4_address: 23.181.64.81/31
      ipv6_address: 2620:136:a009:af00::81/127
      type: gre
      description: SIN1-AUS4 L3 Link MYREP2
      mtu: 1450
      ttl: 255
      remote: 71.78.15.27
      source: 101.100.165.109
      interface: eth1

  SIN2:
    tun202:
      ipv4_address: 23.181.64.2/31
      ipv6_address: 2620:136:a009:af00::2/127
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
      ipv4_address: 23.181.64.61/31
      ipv6_address: 2620:136:a009:af00::61/127
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
      ipv4_address: 23.181.64.63/31
      ipv6_address: 2620:136:a009:af00::63/127
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
      ipv4_address: 23.181.64.70/31
      ipv6_address: 2620:136:a009:af00::70/127
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
      ipv4_address: 23.181.64.72/31
      ipv6_address: 2620:136:a009:af00::72/127
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
      ipv4_address: 23.181.64.4/31
      ipv6_address: 2620:136:a009:af00::4/127
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
      ipv4_address: 23.181.64.65/31
      ipv6_address: 2620:136:a009:af00::65/127
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
      ipv4_address: 23.181.64.67/31
      ipv6_address: 2620:136:a009:af00::67/127
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
      ipv4_address: 23.181.64.74/31
      ipv6_address: 2620:136:a009:af00::74/127
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
      ipv4_address: 23.181.64.76/31
      ipv6_address: 2620:136:a009:af00::76/127
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
