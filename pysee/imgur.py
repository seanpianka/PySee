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
import sys

import requests
import json
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from datetime import datetime

from helpers import init_config
from configs import paths as p


def authenticate_client():
    conf_dir_path = p['config_dir_path']
    conf_file = p['config_file_name']
    config_parser= init_config(conf_dir_path + conf_file)

    client_id = config_parser.get('Imgur_API', 'client_id')
    client_secret = config_parser.get('Imgur_API', 'client_secret')

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
    except FileNotFoundError as e:
        print("There was an issue locating the image file to be uploaded.\n"
              "Error: ", e, "\n")
        return -1
    except ImgurClientError as e:
        print("There was an error validating your API keys for imgur.com.\n" +
              "Go to https://api.imgur.com/oauth2/addclient to receive your" +
              " own API keys.\n"
              "Error " + str(e.status_code) + ": " + str(e.error_message))
        return -2

