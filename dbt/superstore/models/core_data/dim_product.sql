{{ config(
    materialized='incremental',
    unique_key='product_hash_key',
    schema='core'
) }}
WITH new_products AS (
    SELECT DISTINCT 
        MD5(CONCAT("Product ID", '_', "Product Name")) AS product_hash_key, 
        "Product ID" AS product_id,  
        "Product Name" AS product_name,
        "Category" AS category,
        "Sub-Category" AS sub_category
    FROM {{ source('superstore_data', 'superstore_data_raw') }}
)
SELECT 
    product_hash_key,
    product_id,
    product_name,
    category,
    sub_category
FROM new_products
