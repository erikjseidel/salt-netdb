{%- set data = salt.policy.generate() %}

{%- if data['result'] %}

Policy_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      data: {{ data }}

{%- elif data['error'] %}
policy_generate_dictionary_empty:
  test.fail_without_changes:
    - name: {{ data['comment'] }}

{% else %}
noop:
  test.succeed_without_changes:
    - name: {{ data['comment'] }}
{%- endif %}
