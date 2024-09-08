Ethernet_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      ethernet: {{ salt.interface.get_vyos_ethernet() }}
