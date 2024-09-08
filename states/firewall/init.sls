Firewall_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      fw_data: {{ salt.column.pull('firewall') }}
      interfaces: {{ salt.column.pull('interface') }}
