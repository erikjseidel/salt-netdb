Loopback_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      loopbacks: {{ salt.interface.get_vyos_loopbacks() }}
