
{% set categories = dbt_utils.get_column_values(
    table = ref('dim_product'), 
    column = 'category',
) %}

{{
    config(
    materialized='incremental',
    unique_key='order_date',
    schema='dm'
    )
}}

SELECT 
order_date, 
    {% for category in categories %}
        SUM(CASE WHEN category = '{{ category }}' THEN profit END) AS {{ category | replace(' ', '_') | lower }}_profit
        {% if not loop.last %},{% endif %}
    {% endfor %}
, SUM(profit) as total_profit
FROM {{ ref('superstore_sales_t') }}
{% if is_incremental() %}
WHERE order_date >= CURRENT_DATE - INTERVAL '14 days'
{% endif %}
GROUP BY order_date
ORDER BY order_date