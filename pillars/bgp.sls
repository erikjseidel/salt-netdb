#!jinja|yaml

{#

#}

znsl_bgp:
  common:
    timers:
      hold: 30
      keepalive: 10

{% if 'cloud_router' in grains['roles'] %}
  cloud_router:
    asn: 36198
    peer_groups:
      6_RR:
        family:
          ipv6:
            route_map:
              export: 6-RR-OUT
              import: 6-RR-IN
          ipv4:
            route_map:
              export: 4-RR-OUT
              import: 4-RR-IN
        type: ibgp
        source: {{ grains.ibgp_ipv6 }}
    neighbors:
      'fd00:136:a009:af00::227':
        peer_group: 6_RR
      'fd00:136:a009:af00::228':
        peer_group: 6_RR

{%     if 'singapore' in grains['location'] %}
  cloud_router_sin:
    family:
      ipv4:
        networks:
          '170.39.65.0/24':
        redistribute:
          static:
      ipv6:
        networks:
          '::/0':
        redistribute:
          static:

    peer_groups:
      6_SIN_PEER:
        family:
          ipv6:
            route_map:
              export: 6-SIN-PEER-OUT
              import: ALLOW-ALL
          ipv4:
            route_map:
              export: 4-SIN-PEER-OUT
              import: ALLOW-ALL
        type: ibgp
        source: {{ grains.ibgp_ipv6 }}
      4_SIN_65085:
        family:
          ipv4:
            nhs: y
            route_map:
              export: 4-65085-OUT
              import: 4-65085-IN
        type: ebgp
        remote_asn: 65085
      6_SIN_65085:
        family:
          ipv6:
            nhs: y
            route_map:
              export: 6-65085-OUT
              import: 6-65085-IN
        type: ebgp
        remote_asn: 65085
{%     endif %}
{% endif %}

{% if 'vultr' in grains['providers'] %}
  vultr_node:
    peer_groups:
      4_VULTR:
        family:
          ipv4:
            nhs: y
            route_map:
              export: 4-VULTR-OUT
              import: 4-VULTR-IN
        multihop: 2
        type: ebgp
        password: gladstone1
        remote_asn: 64515
      6_VULTR:
        family:
          ipv6:
            nhs: y
            route_map:
              export: 6-VULTR-OUT
              import: 6-VULTR-IN
        multihop: 2
        type: ebgp
        password: gladstone1
        remote_asn: 64515
    neighbors:
      '169.254.169.254':
        peer_group: 4_VULTR
      '2001:19f0:ffff::1':
        peer_group: 6_VULTR
{% endif %}

{% if 'internal_router' in grains['roles'] %}
{%     if 'singapore' in grains['location'] %}

  internal_router_sin:
    family:
      ipv4:
        networks:
          '170.39.65.0/25':
        redistribute:
          static:
          connected:
      ipv6:
        networks:
          '2620:136:a001::/48':
        redistribute:
          static:
          connected:
    peer_groups:
      4_SIN_VULTR:
        family:
          ipv4:
            nhs: y
            route_map:
              export: 4-ZNSL-OUT
              import: 4-ZNSL-IN
        remote_asn: 36198
      6_SIN_VULTR:
        family:
          ipv6:
            nhs: y
            route_map:
              export: 6-ZNSL-OUT
              import: 6-ZNSL-IN
        remote_asn: 36198
      4_AUS_JORGE:
        family:
          ipv4:
            nhs: y
            route_map:
              export: 4-ZNSL-OUT
              import: 4-ZNSL-IN
        remote_asn: 65082
      6_AUS_JORGE:
        family:
          ipv6:
            nhs: y
            route_map:
              export: 6-ZNSL-OUT
              import: 6-ZNSL-IN
        remote_asn: 65082

{%     endif %}
{% endif %}
