"""
imgur
~~~~~

Establish an authorized client and manage
anonimized image-file uploading to Imgur.

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None

.. seealso:: https://api.imgur.com/
"""

import os

import requests
import json
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from datetime import datetime

import helpers
from configs import paths as p


def authenticate_client():
    configuration_file = p['configdir'] + 'config.ini'

    config_ini = helpers.init_config(configuration_file)
    client_id = config_ini.get('Imgur_API', 'client_id')
    client_secret = config_ini.get('Imgur_API', 'client_secret')

    return ImgurClient(client_id, client_secret)


def upload_picture(image_path):
    client = authenticate_client()

    upload_json = {
        'album': None,
        'name': image_path['name'],
        'title': None,
        'description': 'Screenshot taken via PySee'
    }

    print('Uploading screenshot...')
    try:
        return client.upload_from_path(image_path['path'],
                                       config=upload_json,
                                       anon=True)
    except helpers.error.ImgurClientError:
        print("There was an error validating your API keys for imgur.com. Go to https://api.imgur.com/oauth2/addclient to receive your own API keys.\n")
        return None
