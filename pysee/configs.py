#!/usr/bin/python3
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

import helpers

base_config_file_test = """[credentials]
client_id=a764747a577a476
client_secret=42591ec4ba808c69ec7e59534a493525c7538d57
refresh_token=

[path]
config_path=~/.pysee/
base_img_path=~/Pictures/"""
config_file = 'config.ini'

paths = {}

def check_config():
    paths['confdir'] = os.path.expanduser('~/.pysee/')
    if not os.path.exists(paths['confdir']):
        try:
            print("Creating configuration folder...")
            os.makedirs(paths['confdir'])
        except OSError as e:
            if e.errno != errno.EEXIST or not os.path.isdir(paths['confdir']):
                raise
                exit()
    if not os.path.exists(paths['confdir'] + config_file):
        try:
            print("Creating configuration file...")
            with open(paths['confdir'] + config_file, "w") as f:
                f.write(base_config_file_test)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
                exit()
    config_ini = helpers.init_config(paths['confdir'] + config_file)
    paths['imgdir'] = os.path.expanduser(config_ini.get('path', 'base_img_path'))


if __name__ == "__main__":
    check_config()
