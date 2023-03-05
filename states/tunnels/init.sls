{%- set data = salt.tunnel.generate() %}

{%- if data['result'] %}

Tunnel_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
    - data: {{ data }}

{%- elif data['error'] %}
tunnels_generate_dictionary_empty:
  test.fail_without_changes:
    - name: {{ data['comment'] }}

{% else %}
noop:
  test.succeed_without_changes:
    - name: {{ data['comment'] }}
{%- endif %}
