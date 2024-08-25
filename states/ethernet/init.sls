{%- set data = salt.ethernet.generate() %}

{%- if data['result'] %}

Ethernet_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      data: {{ data }}

{%- elif data['error'] %}
ethernet_generate_dictionary_empty:
  test.fail_without_changes:
    - name: "{{ data['comment'] }}"

{% else %}
noop:
  test.succeed_without_changes:
    - name: "{{ data['comment'] }}"
{%- endif %}
