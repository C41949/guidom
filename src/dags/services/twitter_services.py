import tweepy
from airflow.models import Variable
from tweepy import API

from .common_services import get_image_info, save_image, get_now, delete_image


def get_twitter_api_client() -> API:
    consumer_key, consumer_secret = Variable.get('twitter_consumer_key'), Variable.get('twitter_consumer_secret')
    access_key, access_secret = Variable.get('twitter_access_key'), Variable.get('twitter_access_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    return tweepy.API(auth)


def send_direct_message(animal_url: str = None, recipient_id: str = None) -> None:
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
