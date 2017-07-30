import requests

from pysee.hosts import ImageHost


class UploadsimHost(ImageHost):
    """
    uploads_im
    ~~~~~~~~~~

    Format screenshot path and request data
    for uploading to Uploads.im.

    :author: Sean Pianka <me@seanpianka.com>
    :copyright: Copyright 2016 Sean Pianka
    :license: None
    """
    API_URL = "http://uploads.im/api"

    def upload(self, image_path: str):
        with open(image_path['path'], 'rb') as img:
            try:
                response = requests.post(UploadsimHost.API_URL, params={'upload': img})
            except Exception as e:
                raise pye['2']

        if response.json()['status_code']:
            return response.json()['data']
        else:
            raise pye['9']
