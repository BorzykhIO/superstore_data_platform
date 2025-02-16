from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

# Определяем основные параметры DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Создаем DAG
with DAG(
    'dummy_operator_example',
    default_args=default_args,
    description='Simple DAG with DummyOperators',
    schedule_interval=None,  # Этот DAG запускается вручную
    start_date=datetime(2025, 1, 1),  # Указываем стартовую дату
    catchup=False,
) as dag:

    # Создаем задачи
    start = DummyOperator(
        task_id='start',
    )

    task_1 = DummyOperator(
        task_id='task_1',
    )

    task_2 = DummyOperator(
        task_id='task_2',
    )

    end = DummyOperator(
        task_id='end',
    )

    # Определяем зависимости
    start >> [task_1, task_2] >> end
