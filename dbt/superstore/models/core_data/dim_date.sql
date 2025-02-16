{{ config(
    materialized='incremental',
    unique_key='order_date_str',
    schema='core'
) }}

WITH new_dates AS (
    SELECT DISTINCT 
        "Order Date" AS order_date_str,
        "Order Date"::DATE AS full_date,
        date_part('year', "Order Date"::DATE) AS year_number,
        date_part('month', "Order Date"::DATE) AS month_number,
        date_part('day',"Order Date"::DATE) AS day_number,
        TO_CHAR("Order Date"::DATE, 'FMDay') as weekday
    FROM {{ source('superstore_data', 'superstore_data_raw') }}
    {% if is_incremental() %}
    WHERE "Order Date"::DATE NOT IN(SELECT full_date FROM {{ this }})
    {% endif %}
)
SELECT
    order_date_str,
    full_date,
    year_number,
    month_number,
    day_number,
    weekday
FROM new_dates
