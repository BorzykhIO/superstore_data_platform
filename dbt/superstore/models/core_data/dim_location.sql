{{ config(
    materialized='incremental',
    unique_key='location_hash_key',
    schema='core'
) }}

WITH new_locations AS (
    SELECT DISTINCT 
        MD5(CONCAT("Country", "State", "City", "Postal Code")) AS location_hash_key, 
        "Country" AS country, 
        "State" AS state,
        "City" AS city,
        "Postal Code" AS postal_code
    FROM {{ source('superstore_data', 'superstore_data_raw') }}
    {% if is_incremental() %}
    WHERE MD5(CONCAT("Country", "State", "City", "Postal Code")) NOT IN (SELECT location_hash_key FROM {{ this }})
    {% endif %}
)
SELECT  
    location_hash_key,
    country,
    state,
    city,
    postal_code
FROM new_locations
