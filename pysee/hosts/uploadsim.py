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

from pysee.hosts import ImageHost


class UploadsimHost(ImageHost):
    HOST_NAME = "Uploadsim"

    def __init__(self):
        self.api_url = "http://uploads.im/api"

    def upload(self, image_path: str):
        with open(image_path, 'rb') as img:
            try:
                response = requests.post(self.api_url, params={'upload': img})
            except Exception as e:
                raise PySeeError("Unable to upload screenshot to selected image host")

        if response.json()['status_code']:
            return response.json()['data']
        else:
            raise PySeeError("Image host detected an error in image upload attempt")
