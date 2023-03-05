
znsl_firewall:
  custom_firewall:
    zone_policy:
      zone:
        CORE:
          interfaces:
            - bond0.902
            - bond0.17
            - bond0.15
            - l2tp+
        EDGE:
          interfaces:
            - dum23
            - eth0
            - eth1
            - tun370
            - tun372
            - tun374
            - tun376
            - tun378
            - tun380

    mss_clamp:
      ipv6: 1280
      ipv4: 1280
      interfaces:
        - tun370
        - tun372
        - tun374
        - tun376
        - tun378
        - tun380
