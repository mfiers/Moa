% {{ moa_id }}
% {{ template_author }}
% {{ template_modification_date}}
{{ '#' }}NAME
{{ moa_id }}

{{ '#' }} DESCRIPTION 
<<<<<<< HEAD:doc/jinja_templates/template.help.md

{{ d.template_title }}
=======
>>>>>>> 4a1b10035cf299966adcb0540ff0fabbc8556db5:doc/jinja2/help/template.help.md

{{ template_title }}

{% if template_manual %}
{{ template_manual }}
{% endif %}

{{ '#' }} TARGETS
(empty) / {{ moa_id }}
:    {{ template_description }}
{% for target in moa_targets -%}
{% if target != moa_id -%}
{{ target }}
:    {{ d[target + '_help'] }}
{% endif %}
{% endfor %}
{{ '#' }} PARAMETERS
(* denotes a mandatory parameter)
{% for cat in parameter_category_order -%}
{% if cat -%}
{{ '##'}} {{ cat|capitalize }} parameters
{% endif -%}
{% for pn in parameter_categories[cat] -%}
{% set par = parameters[pn] %}
{% if par.mandatory %}*{%- endif %}{{ pn }}
:    {{ par.help }}

     * data type: {{ par.type }}
{%- if par.type == 'set' -%}
{{ ' ' }}({% for a in par.allowed -%}
{% if a == par.default -%}__{% endif -%}{{ a }}
{%- if a == par.default -%}__{% endif -%}
{%- if not loop.last -%}, {% endif -%}
{%- endfor -%})
{%- else -%}
{%- if par.default %}
     * default: `{{ par.default }}`
{%- endif -%}
{%- endif -%}
{%- if par.value %}
     * current value: `{{ par.value }}`
{%- else %}
     * currently not defined
{%- endif %}

{% endfor -%}

{% endfor -%}

{{ '#' }}SEE ALSO 

- http://mfiers.github.com/Moa/ for a online manual
- http://github.com/mfiers/Moa for the github page

{{ '#' }}NOTE 

This page is specific for the ({{ moa_id }}) template. To get more Moa
specific help, please run:

    moa --help
