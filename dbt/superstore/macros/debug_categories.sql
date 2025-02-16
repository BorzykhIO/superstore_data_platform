-- {% macro debug_categories() %}
--     {% set categories_query %}
--         SELECT DISTINCT category FROM dm.superstore_sales_t
--     {% endset %}

--     {% set categories = run_query(categories_query).columns[0].values() if execute else [] %}

--     {% do log("Categories found: " ~ categories, info=True) %}

--     {{ return(categories) }}
-- {% endmacro %}
