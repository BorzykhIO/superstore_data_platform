{{ config(
    materialized='incremental',
    unique_key='order_hash_key',
    schema='core'
) }}

WITH base AS (
    SELECT
        MD5(CONCAT("Order ID", "Order Date", "Product ID", "Customer ID")) AS order_hash_key,
        raw."Order ID" AS order_id,
        dim_customer.customer_hash_key,
        dim_product.product_hash_key,
        dim_location.location_hash_key,
        raw."Order Date" AS order_date,
        raw."Ship Date" AS ship_date,
        raw."Sales" AS sales,
        raw."Quantity" AS quantity,
        raw."Discount" AS discount,
        raw."Profit" AS profit
    FROM {{ source('superstore_data', 'superstore_data_raw') }} raw
    -- Join with Customer Dimension
    LEFT JOIN {{ ref('dim_customer') }} dim_customer
        ON raw."Customer ID" = dim_customer.customer_id
    -- Join with Product Dimension
    LEFT JOIN {{ ref('dim_product') }} dim_product
        ON raw."Product ID" = dim_product.product_id
    -- Join with Location Dimension
    LEFT JOIN {{ ref('dim_location') }} dim_location
        ON raw."Country" = dim_location.country
        AND raw."State" = dim_location.state
        AND raw."City" = dim_location.city
        AND raw."Postal Code" = dim_location.postal_code
    {% if is_incremental() %}
    -- Process only new or updated records
    WHERE MD5(CONCAT("Order ID", "Order Date", "Product ID", "Customer ID")) NOT IN (SELECT order_hash_key FROM {{ this }})
    {% endif %}
)

SELECT * FROM base
