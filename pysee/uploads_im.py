"""
uploads_im
~~~~~~~~~~

Format screenshot path and request data
for uploading to Uploads.im.

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None
"""
import requests
import json

from error import pysee_errors as pye

UPLOADS_API_URL = "http://uploads.im/api"


def upload_picture(image_path):
    with open(image_path['path'], 'rb') as img:
        try:
            response = requests.post(UPLOADS_API_URL, files={'upload':img})
        except Exception as e:
            raise pye['2']

    if response.json()['status_code']:
        return response.json()['data']
    else:
        raise pye['9']
