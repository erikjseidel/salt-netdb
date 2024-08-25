{%- set data = salt.firewall.generate() %}
{%- set interfaces = salt.column.get('interface') -%}

{%- if data['result'] %}

Firewall_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      data: {{ data }}
      interfaces: {{ interfaces }}

{%- elif data['error'] %}
firewall_generate_dictionary_empty:
  test.fail_without_changes:
    - name: "{{ data['comment'] }}"

{% else %}
noop:
  test.succeed_without_changes:
    - name: "{{ data['comment'] }}"
{%- endif %}
