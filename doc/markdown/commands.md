% Moa\_commands
% Mark Fiers
% {{ date_generated }}
# Overview of MOA commands

{% for c in command_order %}
* _{{ c|replace('_', '\_') }}_: {{ commands[c]['desc'] }}
{% endfor %}
