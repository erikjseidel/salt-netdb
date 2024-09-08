ISIS_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      protocol: {{ salt.column.pull('protocol') }}
