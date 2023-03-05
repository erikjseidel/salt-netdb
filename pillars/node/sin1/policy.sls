#!jinja|yaml

znsl_policy:

  custom_policy:
    prefix_lists:
      ipv4:
        4-{{ grains['local_asn'] }}-PREFIXES:
          rules:
            - prefix: 10.0.0.0/8
              le: 24
            - prefix: 170.39.65.0/24
              le: 29
            - prefix: 23.181.64.0/24
              le: 32

      ipv6:
        6-{{ grains['local_asn'] }}-PREFIXES:
          rules:
            - prefix: 2620:136:a001::/48
              le: 64
