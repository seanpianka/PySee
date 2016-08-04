"""
sli.mg
~~~~~

Establish an authorized client and manage
anonimized image-file uploading to SLi.mg

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None

"""
import requests
import json

from error import pysee_errors as pye
from helpers import init_config
from configs import paths as p

API_URL = "https://api.sli.mg/media"


def upload_picture(image_path):
    conf_dir_path = p['config_dir_path']
    conf_file = p['config_file_name']
    config_parser= init_config(conf_dir_path + conf_file)

    client_id = config_parser.get('Slimg_API', 'client_id')
    client_secret = config_parser.get('Slimg_API', 'client_secret')

    with open(image_path['path'], 'rb') as img:
        payload = {
            'key': 'Image uploaded via PySee',
            'type':'binary',
            'data': img
        }
        try:
            response = requests.post(API_URL,
                                     headers={
                                         'Authorization': "Client-ID: " + client_id,
                                     },
                                     data={
                                         'type': 'base64',
                                         'data': img
                                     })
            print(response)
        except Exception as e:
            print(e)
            raise pye['2']

    if response.json()['status_code']:
        return response.json()['data']
    else:
        raise pye['9']
