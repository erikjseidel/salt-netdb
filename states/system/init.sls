System_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      device_data: {{ salt.column.pull('device') }}
      protocol_data: {{ salt.column.pull('protocol') }}
