import os
from datetime import datetime
from typing import Tuple

import requests


def get_now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def get_image_info(image_url: str) -> Tuple[str, str]:
    image_url = requests.get(image_url).json()[0].get('url')
    image_filename = image_url.split('/')[-1]
    return image_url, image_filename


def save_image(filename, image_url) -> None:
    with open(filename, 'wb') as handler:
        handler.write(requests.get(image_url, allow_redirects=True).content)


def delete_image(filename) -> None:
    os.remove(filename)
