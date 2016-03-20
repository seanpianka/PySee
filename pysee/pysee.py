#!/usr/bin/python3
"""
PySee
~~~~~

A lightweight screenshot tool with automatic
Imgur uploading and system clipboard copying.

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None

"""
import os
import errno
import sys
from subprocess import Popen

import imgur
import pyperclip
from datetime import datetime as dt

from configs import paths as p, check_config
from helpers import find_screenshot_tool


def screenshot():
    time_format = r'%Y-%m-%d-%H-%M-%S'

    tool = find_screenshot_tool()

    command = tool.command + ' ' + tool.area + ' ' + tool.filename + ' '
    command += p['imgdir'] + '{}.png 2>/dev/null'
    cmd = Popen([command.format(dt.now().strftime(time_format))], shell=True)
    img_path = p['imgdir'] + '{}.png'.format(dt.now().strftime(time_format))
    cmd.communicate()

    trunc_img_path = img_path.replace(p['imgdir'], '')[:-4]
    image_paths = {
            'full': img_path,           # Screenshot and absolute path
            'trunc': trunc_img_path     # Screenshot with extension only
    }
    return image_paths


def run():
    check_config()
    client = imgur.authenticate_client()
    image_paths = screenshot()
    response = imgur.upload_picture(client, image_paths)
    if response is not None:
        print("Successful upload of {}.png!".format(image_paths['trunc']),
              "\nYou can find it here: {}".format(response['link']),
          "\nIt has also been copied to your system clipboard (Ctrl+V)")
        pyperclip.copy(response['link'])
    else:
        print("There was an error when attempting to save or" +
                "upload the screenshot. Please try again.")

if __name__ == "__main__":
    run()
