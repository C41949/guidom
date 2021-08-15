import os
from datetime import datetime, timedelta
from typing import Tuple
from emoji import unicode_codes, emojize

import random
import requests


ALL_EMOJIS = list(unicode_codes.EMOJI_UNICODE['en'].keys())

def get_now() -> str:
    now = datetime.now() - timedelta(hours=3)
    return now.strftime("%H:%M:%S")


def get_image_info(image_url: str) -> Tuple[str, str]:
    image_url = requests.get(image_url).json()[0].get('url')
    image_filename = image_url.split('/')[-1]
    return image_url, image_filename

def get_emojis_locally(quantity: int = 3):
    random_numbers: list[int] = random.sample(range(0, len(ALL_EMOJIS)), quantity)
    random_emojis: list[str] = [emojize(ALL_EMOJIS[i]) for i in random_numbers] 
    return ' '.join(random_emojis)

# Removed since banned from using the api
def get_emojis(quantity: int = 3) -> str:
    response = requests.get(f'https://api.emojisworld.io/v1/random?limit={quantity}')
    if response.ok:
        data = response.json()
        emoji_list: list[str] = [emoji.get('emoji') for emoji in data.get('results', [])]
        return ' '.join(emoji_list)
        
    return ' '.join(['☀️' for i in range(quantity)])

def save_image(filename, image_url) -> None:
    with open(filename, 'wb') as handler:
        handler.write(requests.get(image_url, allow_redirects=True).content)


def delete_image(filename) -> None:
    os.remove(filename)
