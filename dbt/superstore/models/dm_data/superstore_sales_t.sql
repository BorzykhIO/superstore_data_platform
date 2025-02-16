{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='order_id',
    alias='superstore_sales_t',
    schema='dm'
) }}
with orders AS (
select
o.order_id
, dd.full_date as order_date
, dd.year_number as order_year
, dd.month_number as order_month
, dd.day_number as order_day
, dd.weekday as order_weekday
, dp.product_id
,dp.product_name
,dp.category
,dp.sub_category
,o.ship_date
,cust.customer_id
,cust.customer_name
,cust.segment as customer_segment
,dl.country as order_country
,dl.state as order_state
,dl.city as order_city
,dl.postal_code as order_postal_code
,o.sales
,o.quantity
,o.discount
,o.profit
from {{ref('fact_orders')}} o
left join {{ ref('dim_customer') }}  cust
	on cust.customer_hash_key = o.customer_hash_key 
left join {{ ref('dim_date') }} dd 
	on dd.full_date = cast(o.order_date as date)
left join {{ ref('dim_location') }} dl 
	on dl.location_hash_key = o.location_hash_key 
left join {{ ref('dim_product') }} dp 
	on dp.product_hash_key = o.product_hash_key
)
SELECT 
*
FROM orders
{% if is_incremental() %}
WHERE order_date > (SELECT COALESCE(MAX(order_date), '1900-01-01') FROM {{ this }})
{% endif %}