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

UPLOADS_API_URL = "http://uploads.im/api"


def upload_picture(image_path):
    with open(image_path['path'], 'rb') as img:
        response = requests.post(UPLOADS_API_URL, files={'upload':img})
    if response.json()['status_code'] is 200:
        return response.json()['data']

