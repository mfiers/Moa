% {{ d.moa_id }} 
% {{ d.template_author }}
% {{ d.template_modification_date}}
{{ d.template_title }}
{% if d.template_manual %}
{{ d.template_manual }}
{% endif %}

{{ '#' }} Targets
(empty) / {{ d.moa_id }}
:    {{ d.template_description }}
{% for target in d.moa_targets -%}
{% if target != d.moa_id -%}
{{ target }}
:    {{ d[target + '_help'] }}
{% endif %}
{% endfor %}
{{ '#' }} Parameters
(* denotes a mandatory parameter)
{% for cat in d.parameter_category_order -%}
{% if cat -%}
{{ '##'}} {{ cat }} parameters
{% endif -%}
{% for pn in d.parameter_categories[cat] -%}
{% set par = d.parameters[pn] %}
{{ pn }}{% if par.mandatory %}*{%- endif %} : {{ ' ' }}
{%- if par.value -%}
{{ ' ' }}`{{ par.value }}`
{%- else -%}
{{ ' ' }}(undefined)
{%- endif %}
:    {{ par.help }}  ({{ par.type }}
{%- if par.type == 'set' -%}
: {% for a in par.allowed -%}
{% if a == par.default -%}__{% endif -%}
{{ a }}
{%- if a == par.default -%}__{% endif -%}
{%- if not loop.last %}, {% endif -%}
{%- endfor -%}
{% else %}
{%- if par.default -%}
, default: {{ par.default }}
{%- endif -%}
{%- endif -%}
)
{% endfor -%}

{% endfor -%}
