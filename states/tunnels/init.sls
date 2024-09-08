Tunnel_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      tunnels: {{ salt.interface.get_vyos_tunnels() }}
