{{ config(
    materialized='incremental',
    unique_key='customer_hash_key',
    schema='core'
) }}

WITH new_customers AS (
    SELECT DISTINCT 
        MD5(CONCAT("Customer ID", "Customer Name", "Segment")) as customer_hash_key, 
        "Customer ID" as customer_id, 
        "Customer Name" as customer_name, 
        "Segment" as segment
    FROM {{ source('superstore_data', 'superstore_data_raw') }}
    {% if is_incremental() %}
    -- Загружаем только новые записи (лучше использовать updated_at, если есть)
    WHERE "Customer ID" NOT IN (SELECT customer_id FROM {{ this }})
    {% endif %}
)
SELECT
    customer_hash_key,
    customer_id,
    customer_name,
    segment
FROM new_customers
