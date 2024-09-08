Policy_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      policy_data: {{ salt.column.pull('policy') }}
      interfaces: {{ salt.column.pull('interface') }}
