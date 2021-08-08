import ast

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from services.twitter_services import tweet
from services.common_services import get_emojis

default_args = {'owner': 'airflow', 'depends_on_past': False, 'start_date': '2021-08-06', 'retries': 0}

morning_dag_config = {
    'dag_id': 'send-tweet-good-morning-dag',
    'default_args': default_args,
    'schedule_interval': "0 10 * * *",
    'catchup': False,
}

with DAG(**morning_dag_config) as dag:
    start = DummyOperator(task_id='start', dag=dag)
    end = DummyOperator(task_id='end', dag=dag)

    task = PythonOperator(
            task_id='send-tweet-good-morningt-task',
            python_callable=tweet,
            op_kwargs={'tweet': f'bom dia {get_emojis()}'},
            dag=dag
        )
    start >> task >> end