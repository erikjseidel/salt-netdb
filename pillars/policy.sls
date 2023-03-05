#!jinja|yaml

{#

#}

znsl_policy:

  common:
    route_maps:
      ipv4:
        ALLOW-ALL:
          rules:
            - number: 99
              action: permit
        REJECT-ALL:
          rules:
            - number: 99
              action: deny

    prefix_lists:
      ipv4:
        4-DEFAULT-ROUTE:
          rules:
            - prefix: 0.0.0.0/0
        4-ZNSL-PREFIXES:
          rules:
            - prefix: 10.0.0.0/8
              le: 25
            - prefix: 170.39.64.0/22
              le: 29
            - prefix: 44.76.17.0/24
              le: 29
            - prefix: 23.181.64.0/24
              le: 32

      ipv6:
        6-DEFAULT-ROUTE:
          rules:
            - prefix: ::/0
        6-ZNSL-PREFIXES:
          rules:
            - prefix: 2620:136:a000::/44
              le: 64

{% if 'cloud_router' in grains['roles'] %}
  cloud_router:
    prefix_lists:
      ipv4:
        4-BIG-PREFIXES:
          rules:
            - prefix: 0.0.0.0/0
              ge: 1
              le: 7
        4-SMALL-PREFIXES:
          rules:
            - prefix: 0.0.0.0/0
              ge: 25
              le: 32
        4-MARTIAN-PREFIXES:
          rules:
            - prefix: 0.0.0.0/8
              le: 32
            - prefix: 10.0.0.0/8
              le: 32
            - prefix: 192.168.0.0/16
              le: 32
            - prefix: 172.16.0.0/12
              le: 32
            - prefix: 100.64.0.0/10
              le: 32
            - prefix: 127.0.0.0/8
              le: 32
            - prefix: 169.254.0.0/16
              le: 32
            - prefix: 192.0.0.0/24
              le: 32
            - prefix: 192.0.2.0/24
              le: 32
            - prefix: 198.18.0.0/15
              le: 32
            - prefix: 198.51.100.0/24
              le: 32
            - prefix: 203.0.113.0/24
              le: 32
            - prefix: 224.0.0.0/3
              le: 32
        4-IGP-PREFIXES:
          rules:
            - prefix: 10.0.0.0/8
              le: 24
            - prefix: 23.181.64.0/24
              le: 32
            - prefix: 170.39.64.0/22
              le: 32
            - prefix: 172.16.0.0/12
              ge: 24
        4-ZNSL-OUT-PREFIXES:
          rules:
            - prefix: 170.39.64.0/23
            - prefix: 170.39.65.0/24
            - prefix: 23.181.64.0/24
        4-ZNSL-MT-PREFIXES:
          rules:
            - prefix: 170.39.66.0/24

      ipv6:
        6-BIG-PREFIXES:
          rules:
            - prefix: ::/0
              ge: 1
              le: 15
        6-SMALL-PREFIXES:
          rules:
            - prefix: ::/0
              ge: 49
              le: 128
        6-MARTIAN-PREFIXES:
          rules:
            - prefix: ::/8
              le: 128
            - prefix: 200::/7
              le: 128
            - prefix: 2001::/32
              le: 128
            - prefix: 2001:db8::/32
              le: 128
            - prefix: 2002::/16
              le: 128
            - prefix: 3ffe::/16
              le: 128
            - prefix: 5f00::/8
              le: 128
            - prefix: fc00::/7
              le: 128
            - prefix: fe80::/10
              le: 128
            - prefix: fec0::/10
              le: 128
            - prefix: ff00::/8
              le: 128
        6-IGP-PREFIXES:
          rules:
            - prefix: 2620:136:a000::/44
              ge: 64
            - prefix: fd00::/8
              ge: 64
        6-ZNSL-OUT-PREFIXES:
          rules:
            - prefix: 2620:136:a008::/46
            - prefix: 2620:136:a000::/46
              le: 48

    route_maps:
      ipv4:
{% if grains['downstream_asns'] is defined %}
{%     for asn in grains['downstream_asns'] %}
        4-{{ asn }}-IN:
          rules:
            - number: 30
              continue: 50
              match:
                - community_list: SET-LOCALPREF-50
              set:
                - local_pref: 50
              action: permit
            - number: 35
              continue: 50
              match:
                - community_list: SET-LOCALPREF-150
              set:
                - local_pref: 150
              action: permit
            - number: 45
              continue: 50
              set:
                - local_pref: 100
              action: permit
            - number: 50
              match:
                - prefix_list: 4-ZNSL-PREFIXES
              set:
                - community: '36198:100 additive'
              action: permit
            - number: 99
              action: deny
        4-{{ asn }}-OUT:
          rules:
            - number: 10
              match:
                - prefix_list: 4-DEFAULT-ROUTE
              set:
                - origin: igp
              action: permit
            - number: 20
              match:
                - prefix_list: 4-ZNSL-PREFIXES
              action: permit
            - number: 99
              action: deny
{%     endfor %}
{% endif %}
        4-ISIS-OUT:
          rules:
            - number: 50
              match:
                - prefix_list: 4-IGP-PREFIXES
              action: permit
            - number: 99
              action: deny
        4-RR-IN:
          rules:
            - number: 50
              match:
                - prefix_list: 4-ZNSL-PREFIXES
              action: permit
            - number: 55
              match:
                - as_path: US-LEAK-ROUTES
              set:
                - local_pref: 110
              action: permit
            - number: 99
              action: deny
        4-RR-OUT:
          rules:
            - number: 50
              match:
                - community_list: external
              set:
                - next_hop: {{ grains.ibgp_ipv4 }}
                - local_pref: 20
              action: permit
            - number: 99
              action: permit
        4-SIN-PEER-OUT:
          rules:
            - number: 50
              match:
                - community_list: external
              set:
                - next_hop: {{ grains.ibgp_ipv4 }}
                - local_pref: 100
              action: permit
            - number: 99
              action: permit
        4-VULTR-IN:
          rules:
            - number: 5
              match:
                - prefix_list: 4-MARTIAN-PREFIXES
              action: deny
            - number: 10
              match:
                - prefix_list: 4-BIG-PREFIXES
              action: deny
            - number: 15
              match:
                - prefix_list: 4-SMALL-PREFIXES
              action: deny
            - number: 25
              continue: 30
              set:
                - as_path_exclude: 64515
              action: permit
            - number: 30
              continue: 50
              set:
                - as_path_exclude: 65534
              action: permit
            - number: 50
              match:
                - rpki: valid
              set:
                - community: '36198:100 36198:65012 36198:510 additive'
                - large_community: '36198:100:20473 additive'
              action: permit
            - number: 55
              match:
                - rpki: notfound
              set:
                - community: '36198:100 36198:65023 additive'
                - large_community: '36198:100:20473 additive'
              action: permit
            - number: 60
              set:
                - community: '36198:100 36198:65025 additive'
                - large_community: '36198:100:20473 additive'
              action: permit
            - number: 99
              action: deny
        4-VULTR-OUT:
          rules:
            - number: 40
              match:
                - prefix_list: 4-ZNSL-MT-PREFIXES
              set:
                - community: '20473:6000'
              action: permit
            - number: 50
              match:
                - prefix_list: 4-ZNSL-OUT-PREFIXES
              action: permit
            - number: 99
              action: deny

      ipv6:
{% if grains['downstream_asns'] is defined %}
{%     for asn in grains['downstream_asns'] %}
        6-{{ asn }}-IN:
          rules:
            - number: 30
              continue: 50
              match:
                - community_list: SET-LOCALPREF-50
              set:
                - local_pref: 50
              action: permit
            - number: 35
              continue: 50
              match:
                - community_list: SET-LOCALPREF-150
              set:
                - local_pref: 150
              action: permit
            - number: 45
              continue: 50
              set:
                - local_pref: 100
              action: permit
            - number: 50
              match:
                - prefix_list: 6-ZNSL-PREFIXES
              set:
                - community: '36198:100 additive'
              action: permit
            - number: 99
              action: deny
        6-{{ asn }}-OUT:
          rules:
            - number: 10
              match:
                - prefix_list: 6-DEFAULT-ROUTE
              set:
                - origin: igp
              action: permit
            - number: 20
              match:
                - prefix_list: 6-ZNSL-PREFIXES
              action: permit
            - number: 99
              action: deny
{%     endfor %}
{% endif %}
        6-ISIS-OUT:
          rules:
            - number: 50
              match:
                - prefix_list: 6-IGP-PREFIXES
              action: permit
            - number: 99
              action: deny
        6-RR-IN:
          rules:
            - number: 50
              match:
                - prefix_list: 6-ZNSL-PREFIXES
              action: permit
            - number: 55
              match:
                - as_path: US-LEAK-ROUTES
              set:
                - local_pref: 110
              action: permit
            - number: 99
              action: deny
        6-RR-OUT:
          rules:
            - number: 50
              match:
                - community_list: external
              set:
                - next_hop: {{ grains.ibgp_ipv6 }}
                - local_pref: 20
              action: permit
            - number: 99
              action: permit
        6-SIN-PEER-OUT:
          rules:
            - number: 50
              match:
                - community_list: external
              set:
                - next_hop: {{ grains.ibgp_ipv6 }}
                - local_pref: 100
              action: permit
            - number: 99
              action: permit
        6-VULTR-IN:
          rules:
            - number: 5
              match:
                - prefix_list: 6-MARTIAN-PREFIXES
              action: deny
            - number: 10
              match:
                - prefix_list: 6-BIG-PREFIXES
              action: deny
            - number: 15
              match:
                - prefix_list: 6-SMALL-PREFIXES
              action: deny
            - number: 25
              continue: 30
              set:
                - as_path_exclude: 64515
              action: permit
            - number: 30
              continue: 50
              set:
                - as_path_exclude: 65534
              action: permit
            - number: 50
              match:
                - rpki: valid
              set:
                - community: '36198:100 36198:65012 36198:510 additive'
                - large_community: '36198:100:20473 additive'
              action: permit
            - number: 55
              match:
                - rpki: notfound
              set:
                - community: '36198:100 36198:65023 additive'
                - large_community: '36198:100:20473 additive'
              action: permit
            - number: 60
              set:
                - community: '36198:100 36198:65025 additive'
                - large_community: '36198:100:20473 additive'
              action: permit
            - number: 99
              action: deny
        6-VULTR-OUT:
          rules:
            - number: 50
              match:
                - prefix_list: 6-ZNSL-OUT-PREFIXES
              action: permit
            - number: 99
              action: deny

{% endif %}

{% if 'internal_router' in grains['roles'] %}
  internal_router:
    route_maps:
      ipv4:
        4-ZNSL-IN:
          rules:
            - number: 50
              match:
                - prefix_list: 4-DEFAULT-ROUTE
              set:
                - local_pref: 100
              action: permit
            - number: 60
              match:
                - prefix_list: 4-ZNSL-PREFIXES
              set:
                - local_pref: 100
              action: permit
            - number: 99
              action: deny
        4-ZNSL-OUT:
          rules:
            - number: 50
              match:
                - prefix_list: 4-{{ grains['local_asn'] }}-PREFIXES
              action: permit
            - number: 99
              action: deny

      ipv6:
        6-ZNSL-IN:
          rules:
            - number: 50
              match:
                - prefix_list: 6-DEFAULT-ROUTE
              set:
                - local_pref: 100
              action: permit
            - number: 60
              match:
                - prefix_list: 6-ZNSL-PREFIXES
              set:
                - local_pref: 100
              action: permit
            - number: 99
              action: deny
        6-ZNSL-OUT:
          rules:
            - number: 50
              match:
                - prefix_list: 6-{{ grains['local_asn'] }}-PREFIXES
              action: permit
            - number: 99
              action: deny

{% endif %}
