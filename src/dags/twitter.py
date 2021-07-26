import ast
import os
from datetime import datetime, timedelta
from typing import Tuple, List

import requests
import tweepy
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from tweepy import API


def get_twitter_api_client() -> API:
    consumer_key, consumer_secret = Variable.get('twitter_consumer_key'), Variable.get('twitter_consumer_secret')
    access_key, access_secret = Variable.get('twitter_access_key'), Variable.get('twitter_access_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    return tweepy.API(auth)


def get_now() -> str:
    now = datetime.now() - timedelta(hours=3)
    current_time = now.strftime("%H:%M:%S")
    return current_time


def get_image_info(animal_url: str) -> Tuple[str, str]:
    image_url = requests.get(animal_url).json()[0].get('url')
    image_filename = image_url.split('/')[-1]
    return image_url, image_filename


def save_image(filename, image_url):
    with open(filename, 'wb') as handler:
        handler.write(requests.get(image_url, allow_redirects=True).content)


def delete_image(filename):
    os.remove(filename)


def send_direct_message(animal_url: str = None, recipient_id: str = None):
    image_url, image_filename = get_image_info(animal_url)
    twitter_client = get_twitter_api_client()

    save_image(image_filename, image_url)
    media = twitter_client.media_upload(filename=image_filename)

    delete_image(image_filename)

    twitter_client.send_direct_message(
        recipient_id=recipient_id,
        text=f'Agora são {get_now()}: Hora dos bixinhos!!!',
        attachment_type='media',
        attachment_media_id=media.media_id
    )

    return 'Tweet!!!'


def create_twitter_tasks(dag: DAG, send_direct_message_kwargs: List[dict]):
    start = DummyOperator(task_id='start', dag=dag)
    end = DummyOperator(task_id='end', dag=dag)

    tasks = [
        PythonOperator(
            task_id=config['task_id'],
            python_callable=send_direct_message,
            op_kwargs={'animal_url': config['animal_url'], 'recipient_id': config['recipient_id']},
            dag=dag
        )
        for config in send_direct_message_kwargs
    ]
    start >> tasks >> end


default_args = {'owner': 'airflow', 'depends_on_past': False, 'start_date': '2021-07-25', 'retries': 0}
send_direct_message_kwargs = ast.literal_eval(Variable.get('twitter_messages_config'))

morning_dag_config = {
    'dag_id': 'send-twitter-message-dag-morning',
    'default_args': default_args,
    'schedule_interval': "0 8 * * *",
    'catchup': False,
}
afternoon_dag_config = {
    'dag_id': 'send-twitter-message-dag-afternoon',
    'default_args': default_args,
    'schedule_interval': "0 15 * * *",
    'catchup': False,
}
night_dag_config = {
    'dag_id': 'send-twitter-message-dag-night',
    'default_args': default_args,
    'schedule_interval': "0 21 * * *",
    'catchup': False,
}

morning_dag = DAG(**morning_dag_config)
create_twitter_tasks(morning_dag, send_direct_message_kwargs)

afternoon_dag = DAG(**afternoon_dag_config)
create_twitter_tasks(afternoon_dag, send_direct_message_kwargs)

night_dag = DAG(**night_dag_config)
create_twitter_tasks(night_dag, send_direct_message_kwargs)
