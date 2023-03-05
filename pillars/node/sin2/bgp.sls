znsl_bgp:
  node_sin2:
    router_id: 23.181.64.236
    peer_groups:
      4_VULTR:
        source: 139.180.130.102
      6_VULTR:
        source: 2401:c080:1400:6be6:5400:04ff:fe43:c868
    neighbors:
      'fd00:136:a009:af00::237':
        peer_group: 6_SIN_PEER
      '2620:136:a009:af00::71':
        peer_group: 6_SIN_65085
      '2620:136:a009:af00::73':
        peer_group: 6_SIN_65085
      '23.181.64.71':
        peer_group: 4_SIN_65085
      '23.181.64.73':
        peer_group: 4_SIN_65085
