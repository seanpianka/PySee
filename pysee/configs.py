"""
configs
~~~~~~~

Ensure necessary configuration files and directories
are located within the user's home directory.

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None
"""
import os
import sys

import pyperclip

from helpers import init_config
from error import pysee_errors as pye

# Known hosts lists, used when checking for arguments
supported_hosts = ['imgur', 'uploads']
supported_modes = ['region', 'window', 'full']

# Base location and name of config dir and .conf file
paths = {}
config_file_name = 'config.conf'
paths['config_dir_path'] = os.path.expanduser('~/.config/pysee/')
paths['config_file_name'] = config_file_name
base_config_file_contents = """[Imgur_API]
client_id=YOUR_ID_HERE
client_secret=YOUR_SECRET_HERE
refresh_token=

[path]
config_dir_path=~/.config/pysee/
base_img_path=~/Pictures/"""


def verify_configuration():
    conf_dir_path = paths['config_dir_path']
    conf_file = paths['config_file_name']

    if os.path.exists(conf_dir_path) is False:
        try:
            print("Creating configuration folder...")
            os.makedirs(conf_dir_path)
        except OSError as e:
            if e.errno != errno.EEXIST or not os.path.isdir():
                raise pye['7']

    if os.path.exists(conf_dir_path + conf_file) is False:
        try:
            print("Creating configuration file...")
            with open(conf_dir_path + conf_file, "w") as f:
                f.write(base_config_file_contents)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise pye['7']

    config_parser = init_config(conf_dir_path + conf_file)
    paths['imgdir'] = os.path.expanduser(config_parser.get('path', 'base_img_path'))

    try:
        pyperclip.copy('0')
    except pyperclip.exceptions.PyperclipException:
        raise pye['6']


if __name__ == "__main__":
    verify_configuration()
