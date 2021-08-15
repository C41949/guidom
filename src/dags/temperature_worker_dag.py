
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from services.common_services import create_temperature

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '2021-08-06',
    'retries': 0
}

temperature_worker_args = {
    'dag_id': 'create-a-temperature-worker',
    'default_args': default_args,
    'schedule_interval': "* * * * *",
    'catchup': False,
}

with DAG(**temperature_worker_args) as dag:
    start = DummyOperator(task_id='start', dag=dag)
    post = PythonOperator(task_id='create-a-temperature-request', python_callable=create_temperature, dag=dag)
    end = DummyOperator(task_id='end', dag=dag)

    start >> post >> end