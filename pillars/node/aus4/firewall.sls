
znsl_firewall:
  custom_firewall:
    zone_policy:
      zone:
        CORE:
          interfaces:
            - eth6.717
            - eth6.66
            - eth6.902
        EDGE:
          interfaces:
            - tun356
            - tun354
            - eth2
            - tun358
            - tun378
            - tun380
            - dum23

    mss_clamp:
      ipv6: 1280
      ipv4: 1280
      interfaces:
        - tun354
        - tun356
        - tun358
        - tun378
        - tun380
