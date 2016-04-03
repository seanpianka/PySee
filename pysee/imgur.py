#!/usr/bin/python3
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
        response = client.upload_from_path(image_path['path'],
                                           config=upload_json,
                                           anon=True)
    except:
        return None

if __name__ == "__main__":
    pass
