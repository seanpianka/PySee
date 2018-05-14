import os
import logging

import imgurpython
import requests

from utils import get_config_value
from logger import PySeeLogger


logger = PySeeLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)


def _imgur_upload(image_path, title):
    """

    Args:
        image_path:
        title:

    Returns:

    """
    client_id = get_config_value('Imgur', 'client_id')
    client_secret = get_config_value('Imgur', 'client_secret')
    client = imgurpython.ImgurClient(client_id, client_secret)

    try:
        config = {'album': "",
                  'name': os.path.split(image_path)[-1],
                  'title': title,
                  'description': 'Screenshot taken via PySee'}

        response = client.upload_from_path(image_path, config=config, anon=True)
        logger.debug("Imgur upload via imgurpython was successful.")
        return response['link']
    except imgurpython.helpers.error.ImgurClientError:
        logger.exception("There was an error validating your API keys for imgur.com.\n" +
                          "Go to https://api.imgur.com/oauth2/addclient to receive your" +
                          " own API keys.\n")
        raise


def _uploadsim_upload(image_path, title):
    """

    Args:
        image_path:
        title:

    Returns:

    """
    api_url = "http://ufileploads.im/api"

    with open(image_path, 'rb') as img:
        try:
            response = requests.get(api_url, files={'upload': img})
            logger.debug("Uploadsim upload via POST was successful.")
        except requests.exceptions.RequestException:
            logger.error("Unable to upload screenshot to selected image host.")
            raise

    if response.json()['status_code']:
        return response.json()['data']

    return None


HOSTS = {'imgur': _imgur_upload,
         'uploadsim': _uploadsim_upload}
