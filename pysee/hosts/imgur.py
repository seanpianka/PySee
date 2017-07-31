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
import sys
import os

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

from pysee.hosts import ImageHost
from pysee.exceptions import PySeeError


class ImgurHost(ImageHost):
    HOST_NAME = "Imgur"

    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.client = ImgurClient(self.api_keys['client_id'],
                                  self.api_keys['client_secret'])

    def upload(self, image_path: str):
        try:
            config = {'album': "",
                      'name': os.path.split(image_path)[-1],
                      'title': "",
                      'description': 'Screenshot taken via PySee'}

            return self.client.upload_from_path(image_path, config=config, anon=True)
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
        except ImgurClientError as e:
            print("There was an error validating your API keys for imgur.com.\n" +
                  "Go to https://api.imgur.com/oauth2/addclient to receive your" +
                  " own API keys.\n")
            raise PySeeError("Image host detected an error in image upload attempt: {}".format(str(e)))
