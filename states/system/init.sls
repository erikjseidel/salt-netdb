{%- set device_data = salt.column.get('device') %}
{%- set protocol_data = salt.column.get('protocol') %}

{%- if device_data.get('error') %}
system_get_device_column_error:
  test.fail_without_changes:
    - name: "{{ device_data['comment'] }}"

{%- elif protocol_data.get('error') %}
system_get_protocol_column_error:
  test.fail_without_changes:
    - name: "{{ protocol_data['comment'] }}"

{%- elif device_data and protocol_data %}
System_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      device_data: {{ device_data }}
      protocol_data: {{ protocol_data }}

{%- else %}
system_column_empty:
  test.fail_without_changes:
    - name: "Empty column return"
{%- endif %}
