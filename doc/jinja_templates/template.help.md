% {{ d.moa_id }}
% {{ d.template_author }}
% {{ d.template_modification_date}}
{{ '#' }}NAME
{{ d.moa_id }}

{{ '#' }} DESCRIPTION {{ d.template_title }}

{% if d.template_manual %}
{{ d.template_manual }}
{% endif %}

{{ '#' }} TARGETS
(empty) / {{ d.moa_id }}
:    {{ d.template_description }}
{% for target in d.moa_targets -%}
{% if target != d.moa_id -%}
{{ target }}
:    {{ d[target + '_help'] }}
{% endif %}
{% endfor %}
{{ '#' }} PARAMETERS
(* denotes a mandatory parameter)
{% for cat in d.parameter_category_order -%}
{% if cat -%}
{{ '##'}} {{ cat|capitalize }} parameters
{% endif -%}
{% for pn in d.parameter_categories[cat] -%}
{% set par = d.parameters[pn] %}
{% if par.mandatory %}*{%- endif %}{{ pn }}
:    {{ par.help }}  
     
     * data type: {{ par.type }}
{%- if par.type == 'set' -%}
{{ ' ' }}({% for a in par.allowed -%}
{% if a == par.default -%}__{% endif -%}
{{ a }}
{%- if a == par.default -%}__{% endif -%}
{%- if not loop.last %}, {% endif -%}
{%- endfor -%})
{% else %}
{%- if par.default %}
    * default: {{ par.default }}
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
