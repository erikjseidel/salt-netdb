{%- set data = salt.isis.generate() %}

{%- if data['result'] %}

ISIS_Configuration:
  netconfig.managed:
    - template_name: salt://{{ slspath }}/templates/{{ grains.os }}.jinja
      data: {{ data }}

{%- elif not data['result'] %}
isis_generate_dictionary_empty:
  test.fail_without_changes:
    - name: "{{ data['comment'] }}"

{% else %}
noop:
  test.succeed_without_changes:
    - name: "{{ data['comment'] }}"
{%- endif %}
