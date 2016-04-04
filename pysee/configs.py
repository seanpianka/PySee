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
import sys

import pyperclip

from helpers import init_config

config_file = 'config.ini'
paths = {}
base_config_file_test = """[Imgur_API]
client_id=YOUR_ID_HERE
client_secret=YOUR_SECRET_HERE
refresh_token=

[path]
config_path=~/.pysee/
base_img_path=~/Pictures/"""


def verify_configuration():
    paths['configdir'] = os.path.expanduser('~/.pysee/')

    if os.path.exists(paths['configdir']) is False:
        try:
            print("Creating configuration folder...")
            os.makedirs(paths['configdir'])
        except OSError as e:
            if e.errno != errno.EEXIST or not os.path.isdir(paths['configdir']):
                raise
                exit()
    if os.path.exists(paths['configdir'] + config_file) is False:
        try:
            print("Creating configuration file...")
            with open(paths['configdir'] + config_file, "w") as f:
                f.write(base_config_file_test)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
                exit()

    config_ini = init_config(paths['configdir'] + config_file)
    paths['imgdir'] = os.path.expanduser(config_ini.get('path', 'base_img_path'))

    try:
        pyperclip.copy('0')
    except pyperclip.exceptions.PyperclipException:
        print("ERROR: Unable to locate copy/paste mechanism for your system.\n" +
              "Considering perform one of the following commands:\n" +
              "\t'sudo apt-get install xsel'\n" +
              "\t'sudo apt-get install xclip'\n")
        sys.exit(3)

    return None


if __name__ == "__main__":
    verify_configuration()
