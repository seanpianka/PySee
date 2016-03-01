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



paths = {}
paths['confdir'] = os.path.expanduser('~/.pyscreen/')
config_ini = helpers.init_config(paths['confdir'] + 'config.ini')
paths['imgdir'] = os.path.expanduser(config_ini.get('path', 'base_img_path'))

if not os.path.exists(paths['confdir']):
    try:
        os.makedirs(paths['confdir'])
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(paths['confdir']):
            raise
            exit()

if __name__ == "__main__":
    exit()
