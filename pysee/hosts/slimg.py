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

from pysee.hosts import ImageHost
from pysee.exceptions import PySeeError


class SlimgHost(ImageHost):
    HOST_NAME = "Slimg"

    def __init__(self):
        self.api_url = "https://api.sli.mg/media"
        self.api_keys = api_keys

    def upload(self, image_path):
        with open(image_path, 'rb') as img:
            payload = {'key': 'Image uploaded via PySee',
                       'type': 'binary',
                       'data': img}
            try:
                response = requests.post(
                    self.api_url,
                    headers={'Authorization': ''.join(["Client-ID: ", self.api_keys['client_id']])},
                    data={'type': 'base64', 'data': img}
                )
            except requests.exceptions.RequestException as e:
                raise PySeeError("Unable to upload screenshot to selected image host: {}".format(str(e)))

        if response.json()['status_code']:
            return response.json()['data']

        raise PySeeError("Image host detected an error in image upload attempt")
