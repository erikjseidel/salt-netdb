#!jinja|yaml

{#

#}

znsl_firewall:
  common:
    options:
      all-ping: enable
      config-trap: disable
      broadcast-ping: disable
      ipv6-src-route: disable
      ipv6-receive-redirects: disable
      log-martians: enable
      send-redirects: enable
      source-validation: disable
      syn-cookies: enable
      twa-hazards-protection: disable

    groups:
      ipv4:
        martians4:
          type: network
          networks:
            - 10.0.0.0/8
            - 192.168.0.0/16
            - 172.16.0.0/12
            - 100.64.0.0/10
            - 127.0.0.0/8
            - 169.254.0.0/16
            - 192.0.0.0/24
            - 192.0.2.0/24
            - 198.18.0.0/15
            - 198.51.100.0/24
            - 203.0.113.0/24
            - 224.0.0.0/3
            - 0.0.0.0/8
        znsl4:
          type: network
          networks:
            - 170.39.64.0/22
            - 23.181.64.0/24
            - 44.76.17.0/24
        znsl1918:
          type: network
          networks:
            - 10.0.0.0/8
            - 172.16.0.0/12

      ipv6:
        martians6:
          type: network
          networks:
            - ::/8
            - 200::/7
            - 2001::/32
            - 2001:db8::/32
            - 2002::/16
            - 3ffe::/16
            - 5f00::/8
            - fc00::/7
            - fe80::/10
            - fec0::/10
            - ff00::/8
        znsl6:
          type: network
          networks:
            - 2620:136:a000::/44
        znsl4193:
          type: network
          networks:
            - fd00::/8

{% if 'cloud_router' in grains['roles'] %}
  cloud_router:
    options:
      receive-redirect: disable
      ip-src-route: disable

    policies:
      ipv4:
        INTERNAL-LOCAL:
          default_action: drop
          rules:
            - action: accept
              protocol: isis
            - action: accept
              protocol: ospf
            - action: accept
              source:
                - network_group: znsl4
            - action: accept
              source:
                - network_group: znsl1918
            - action: accept
              protocol: tcp_udp
              state: 
                - established
            - action: accept
              protocol: tcp_udp
              state: 
                - related
            - action: accept
              protocol: icmp
            - action: accept
              protocol: gre
            - action: accept
              destination:
                - port:
                    - 500
                    - 4500
              protocol: udp
            - action: accept
              protocol: esp
            - action: accept
              destination:
                - port:
                    - 22
                    - 179
              protocol: tcp
        LOOPBACK-LOCAL:
          default_action: drop
          rules:
            - action: accept
              destination:
                - port:
                    - 22
              protocol: tcp
            - action: accept
              destination:
                - port:
                    - 179
              protocol: tcp
            - action: accept
              source:
                - network_group: znsl4
            - action: accept
              source:
                - network_group: znsl1918
            - action: accept
              protocol: tcp_udp
              state: 
                - established
            - action: accept
              protocol: tcp_udp
              state: 
                - related
            - action: accept
              protocol: icmp
            - action: accept
              destination:
                - port:
                    - 500
                    - 4500
              protocol: udp
            - action: accept
              protocol: esp
            - action: accept
              protocol: gre
        TRANSIT-IN:
          default_action: drop
          rules:
            - action: drop
              source:
                - network_group: martians4
            - action: accept
              destination:
                - network_group: znsl4
        TRANSIT-OUT:
          default_action: drop
          rules:
            - action: drop
              destination:
                - network_group: martians4
            - action: accept
              source:
                - network_group: znsl4
        TRANSIT-LOCAL:
          default_action: drop
          rules:
            - action: accept
              protocol: tcp_udp
              state: 
                - established
            - action: accept
              protocol: tcp_udp
              state: 
                - related
            - action: accept
              protocol: gre
            - action: accept
              destination:
                - port:
                    - 179
              protocol: tcp
            - action: accept
              destination:
                - port:
                    - 22
              protocol: tcp
            - action: accept
              protocol: icmp
            - action: accept
              protocol: esp
            - action: accept
              destination:
                - port:
                    - 500
                    - 4500
              protocol: udp

      ipv6:
        6-INTERNAL-LOCAL:
          default_action: drop
          rules:
            - action: accept
              protocol: isis
            - action: accept
              protocol: ospf
            - action: accept
              source:
                - network_group: znsl6
            - action: accept
              source:
                - network_group: znsl4193
            - action: accept
              protocol: tcp_udp
              state: 
                - established
            - action: accept
              protocol: tcp_udp
              state: 
                - related
            - action: accept
              protocol: icmpv6
        6-LOOPBACK-LOCAL:
          default_action: drop
          rules:
            - action: accept
              destination:
                - port:
                    - 22
              protocol: tcp
            - action: accept
              destination:
                - port:
                    - 179
              protocol: tcp
            - action: accept
              source:
                - network_group: znsl6
            - action: accept
              source:
                - network_group: znsl4193
            - action: accept
              protocol: tcp_udp
              state: 
                - established
            - action: accept
              protocol: tcp_udp
              state: 
                - related
            - action: accept
              protocol: icmpv6
        6-TRANSIT-IN:
          default_action: drop
          rules:
            - action: drop
              source:
                - network_group: martians6
            - action: accept
              destination:
                - network_group: znsl6
        6-TRANSIT-OUT:
          default_action: drop
          rules:
            - action: drop
              destination:
                - network_group: martians6
            - action: accept
              source:
                - network_group: znsl6
        6-TRANSIT-LOCAL:
          default_action: drop
          rules: 
            - action: accept
              protocol: tcp_udp
              state: 
                - established
            - action: accept
              protocol: tcp_udp
              state: 
                - related
            - action: accept
              destination:
                - port:
                    - 179
              protocol: tcp
            - action: accept
              destination:
                - port:
                    - 22
              protocol: tcp
            - action: accept
              protocol: icmpv6

{% endif %}
{% if 'firewall' in grains['roles'] %}
  firewall:
    options:
      receive-redirect: enable
      ip-src-route: enable

    policies:
      ipv4:
        ZNSL-V4:
          default_action: drop
          rules:
            - action: accept
              source:
                - network_group: znsl4
            - action: accept
              source:
                - network_group: znsl1918
            - action: accept
              state:
                - established
                - related
            - action: accept
              protocol: icmp
        CORE-OUT:
          default_action: accept

      ipv6:
        ZNSL-V6:
          default_action: drop
          rules:
            - action: accept
              source:
                - network_group: znsl6
            - action: accept
              state:
                - established
                - related
            - action: accept
              protocol: icmpv6
        CORE-OUT6:
          default_action: accept

    state_policy:
      established: accept
      related: accept

    zone_policy:
      zone:
        CORE:
          default_action: drop
          from:
            - zone: EDGE 
              ipv6_ruleset: ZNSL-V6
              ipv4_ruleset: ZNSL-V4
        EDGE:
          default_action: drop
          from:
            - zone: CORE
              ipv6_ruleset: CORE-OUT6
              ipv4_ruleset: CORE-OUT

{% endif %}
