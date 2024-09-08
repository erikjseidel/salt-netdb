BGP_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      data: {{ salt.column.pull('bgp') }}
