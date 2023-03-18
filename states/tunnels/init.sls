{%- set data = salt.tunnel.generate() %}

{%- if data['result'] %}

Tunnel_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
    - data: {{ data }}

{%- elif not data['result']  %}
tunnel_generate_empty:
  test.fail_without_changes:
    - name: "{{ data['comment'] }}"

{% else %}
noop:
  test.succeed_without_changes:
    - name: "{{ data['comment'] }}"
{%- endif %}
