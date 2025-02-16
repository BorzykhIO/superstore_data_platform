import os
from airflow.operators.bash import BashOperator
from airflow import DAG
from datetime import datetime


dag_id = os.path.splitext(os.path.basename(__file__))[0]

dag = DAG(
    dag_id,
    schedule_interval="@daily",
    start_date=datetime(2024, 2, 7),
    catchup=False
)

dim_location = BashOperator(
    task_id="run_dbt_dim_location",
    bash_command="cd /dbt/superstore/ && dbt run --select dim_location",
    dag=dag
    )

dim_customer = BashOperator(
    task_id="run_dbt_dim_customer",
    bash_command="cd /dbt/superstore/ && dbt run --select dim_customer",
    dag=dag
    )

dim_date = BashOperator(
    task_id="run_dbt_dim_date",
    bash_command="cd /dbt/superstore/ && dbt run --select dim_date",
    dag=dag
    )

dim_product = BashOperator(
    task_id="run_dbt_dim_product",
    bash_command="cd /dbt/superstore/ && dbt run --select dim_product",
    dag=dag
    )

fact_orders = BashOperator(
    task_id="run_dbt_fact_orders",
    bash_command="cd /dbt/superstore/ && dbt run --select fact_orders",
    dag=dag
    )

dm_superstore_sales_t = BashOperator(
    task_id="run_dbt_dm_superstore_sales_t",
    bash_command="cd /dbt/superstore/ && dbt run --select superstore_sales_t",
    dag=dag
    )

dm_categories_pivot_t = BashOperator(
    task_id="run_dbt_dm_categories_pivot_t",
    bash_command="cd /dbt/superstore/ && dbt run --select categories_pivot_t",
    dag=dag
    )

[dim_location, dim_customer, dim_date, dim_product] >> fact_orders >> dm_superstore_sales_t >> dm_categories_pivot_t
