znsl_bgp:
  node_sin3:
    router_id: 23.181.64.237
    peer_groups:
      4_VULTR:
        source: 66.42.59.36
      6_VULTR:
        source: 2001:19f0:4401:d01:5400:4ff:fe44:1d0d
    neighbors:
      'fd00:136:a009:af00::236':
        peer_group: 6_SIN_PEER
      '2620:136:a009:af00::75':
        peer_group: 6_SIN_65085
      '2620:136:a009:af00::77':
        peer_group: 6_SIN_65085
      '23.181.64.75':
        peer_group: 4_SIN_65085
      '23.181.64.77':
        peer_group: 4_SIN_65085
