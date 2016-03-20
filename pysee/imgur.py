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
    config_ini = helpers.init_config(p['configdir'] + 'config.ini')
    client_id = config_ini.get('credentials', 'client_id')
    client_secret = config_ini.get('credentials', 'client_secret')
    return ImgurClient(client_id, client_secret)


def upload_picture(client, image_paths):
    print('Uploading screenshot...')

    conf = {
        'album': None,
        'name': image_paths['trunc'],
        'title': None,
        'description': 'Screenshot taken via PySee'
    }
    try:
        return client.upload_from_path(image_paths['full'], config=conf, anon=True)
    except:
        return None

if __name__ == "__main__":
    pass
