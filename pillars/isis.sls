#!jinja|yaml

{#

#}

{% if 'cloud_router' in grains['roles'] %}
znsl_isis:
  level: 2
  lsp_mtu: 1447
  iso: {{ grains['iso'] }}
  redistribute:
    ipv4:
      level_2:
        connected_map: 4-ISIS-OUT
    ipv6:
      level_2:
        connected_map: 6-ISIS-OUT
  
{% endif %}
