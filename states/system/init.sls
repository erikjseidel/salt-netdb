{%- set data = salt.column.get('device') %}

{%- if data.get('error') %}
system_get_column_error:
  test.fail_without_changes:
    - name: "{{ data['comment'] }}"

{%- elif data %}
System_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      data: {{ data }}

{%- else %}
system_column_empty:
  test.fail_without_changes:
    - name: "Empty column return"
{%- endif %}
