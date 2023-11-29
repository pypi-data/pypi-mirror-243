{% set ns = namespace(transformed_value='') %}

{% set ns1 = namespace(transformation_types = {
    'REM_SPECIAL_CHAR': "REGEXP_REPLACE(column_name,'[^a-zA-Z0-9 ]','')",
    'TRIM_SPACE': "REPLACE(column_name,' ')",
    'LOWER_CASE': "LOWER(column_name)",
    'UPPER_CASE': "UPPER(column_name)",
    'ADD_PREFIX': "CONCAT(value, column_name)",
    'ADD_SUFFIX': "CONCAT(column_name, value)",
    'REPL_VALUE': "REPLACE(column_name, value1, value2)",
    'ABS': "ABS(column_name)",
    'ROUND_UP': "CEIL(column_name, value)",
    'ROUND_DOWN': "FLOOR(column_name, value)",
    'CONVERT_DATE': "TO_DATE(column_name)",
    'TRUNC': "SUBSTR(column_name, value1, value2)",
    'RIGHT': "RIGHT(column_name, LEN(column_name)-value)",
    'LEFT': "LEFT(column_name, LEN(column_name)-value)",
    'SPLIT_COLUMN': "TO_VARCHAR(SPLIT(column_name, value))",
    'FILL_BLANKS': "COALESCE(NULLIF(column_name,''), value)",
	'CONVERT_DATE_OUTBOUND': "TO_VARCHAR(column_name,value)",
    'ROUND_OFF': "ROUND(column_name, value)"
    })
%}

{% set function_name = transform_details['sysName'] %}
{% set function_type = transform_details['type'] %}
{% set ns.transformed_value = ns1.transformation_types[function_name] ~ ' AS "' ~ column_name ~ '"' %}
{% set ns.transformed_value = ns.transformed_value.replace('column_name', '"' ~ column_name ~ '"') %}

{% if function_type == 'TEXT' or function_type == 'DROPDOWN:DATE_FORMAT' %}
    {% set function_input = transform_details['value'] %}
    {% set ns.transformed_value = ns.transformed_value.replace('value', add_quotes(function_input)) %}
{% elif function_type == 'RANGE' %}
    {% set function_input = transform_details['value'] %}
    {% set value1 = (function_input|string).split(':')[0] %}
    {% set value2 = (function_input|string).split(':')[1] %}
    {% set ns.transformed_value = ns.transformed_value.replace('value1', add_quotes(value1)) %}
    {% set ns.transformed_value = ns.transformed_value.replace('value2', add_quotes(value2)) %}
{% endif %}

{{ return(ns.transformed_value) }}