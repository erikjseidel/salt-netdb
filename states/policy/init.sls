{%- set data = salt.policy.generate() %}
{%- set interfaces = salt.column.get('interface') -%}

{%- if data['result'] %}

Policy_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      data: {{ data }}
      interfaces: {{ interfaces }}

{%- elif data['error'] %}
policy_generate_dictionary_empty:
  test.fail_without_changes:
    - name: {{ data['comment'] }}

{% else %}
noop:
  test.succeed_without_changes:
    - name: {{ data['comment'] }}
{%- endif %}
