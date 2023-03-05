znsl_bgp:
  node_sin1:
    router_id: 23.181.64.233
    log_neighbor_changes: y
    neighbors:
      '23.181.64.70':
        peer_group: 4_SIN_VULTR
      '23.181.64.72':
        peer_group: 4_SIN_VULTR
      '23.181.64.74':
        peer_group: 4_SIN_VULTR
      '23.181.64.76':
        peer_group: 4_SIN_VULTR
      '23.181.64.78':
        peer_group: 4_AUS_JORGE
      '23.181.64.80':
        peer_group: 4_AUS_JORGE
      '2620:136:a009:af00::70':
        peer_group: 6_SIN_VULTR
      '2620:136:a009:af00::72':
        peer_group: 6_SIN_VULTR
      '2620:136:a009:af00::74':
        peer_group: 6_SIN_VULTR
      '2620:136:a009:af00::76':
        peer_group: 6_SIN_VULTR
      '2620:136:a009:af00::78':
        peer_group: 6_AUS_JORGE
      '2620:136:a009:af00::80':
        peer_group: 6_AUS_JORGE
