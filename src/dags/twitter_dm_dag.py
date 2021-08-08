import ast
from typing import List

from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from services.twitter_services import send_direct_message


def create_twitter_tasks(dag: DAG, send_direct_message_params: List[dict]) -> None:
    start = DummyOperator(task_id='start', dag=dag)
    end = DummyOperator(task_id='end', dag=dag)

    tasks = [
        PythonOperator(
            task_id=config['task_id'],
            python_callable=send_direct_message,
            op_kwargs={'animal_url': config['animal_url'], 'recipient_id': config['recipient_id']},
            dag=dag
        )
        for config in send_direct_message_params
    ]
    start >> tasks >> end


default_args = {'owner': 'airflow', 'depends_on_past': False, 'start_date': '2021-07-25', 'retries': 0}
send_direct_message_kwargs = ast.literal_eval(Variable.get('twitter_messages_config'))

morning_dag_config = {
    'dag_id': 'send-twitter-message-dag-morning',
    'default_args': default_args,
    'schedule_interval': "6 11 * * *",
    'catchup': False,
}
afternoon_dag_config = {
    'dag_id': 'send-twitter-message-dag-afternoon',
    'default_args': default_args,
    'schedule_interval': "6 18 * * *",
    'catchup': False,
}
night_dag_config = {
    'dag_id': 'send-twitter-message-dag-night',
    'default_args': default_args,
    'schedule_interval': "6 0 * * *",
    'catchup': False,
}

morning_dag = DAG(**morning_dag_config)
create_twitter_tasks(morning_dag, send_direct_message_kwargs)

afternoon_dag = DAG(**afternoon_dag_config)
create_twitter_tasks(afternoon_dag, send_direct_message_kwargs)

night_dag = DAG(**night_dag_config)
create_twitter_tasks(night_dag, send_direct_message_kwargs)
