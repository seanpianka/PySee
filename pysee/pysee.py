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

import pyperclip
import imgur
from datetime import datetime as dt

import uploads_im
from configs import paths as p, verify_configuration
from helpers import find_screenshot_tool

error_msg = "There was an error when attempting to save " + \
            "or upload the screenshot. Please try again."


def capture_screenshot(tool, image_path):
    time_format = r'%Y-%m-%d-%H-%M-%S'

    command = tool.command + ' ' + tool.area + ' ' + tool.filename + ' '
    command += p['imgdir'] + '{}.png 2>/dev/null'
    cmd = Popen([command.format(dt.now().strftime(time_format))], shell=True)
    img_path = p['imgdir'] + dt.now().strftime(time_format) + '.png'
    cmd.communicate()

    img_name = img_path.replace(p['imgdir'], '')[:-4]
    image_path['path'] = img_path  # absolute path of screenshot
    image_path['name'] = img_name  # filename of screenshot

    return None


def upload_screenshot(image_host, image_path):
    try:
        if image_host is "Imgur" or image_host is "I":
            response = imgur.upload_picture(image_path)
            image_url = response['link']
        elif image_host is "Uploads" or image_host is "U":
            response = uploads_im.upload_picture(image_path)
            image_url = response['img_url']
        elif image_host is None or image_host is 0:
            image_url = 0

        return image_url
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return None


def take_screenshot(event=None, root=None,
                    image_host="U", clipboard=True, output=True):
    verify_configuration()

    screenshot_tool = find_screenshot_tool()
    image_path = {}
    capture_screenshot(screenshot_tool, image_path)
    image_url = upload_screenshot(image_host, image_path)

    if image_url is not None and image_url is not "":
        if image_url is 0:
            if output is True:
                print("Successful screenshot!" + \
                      "{} was saved locally.".format(image_path['path']))
            image_url = image_path['path']
        else:
            if output is True:
                print("Successful upload of {}.png!".format(image_path['name']),
                  "\nYou can find it here: {}".format(image_url))
            upload_success = True
        if clipboard is True:
            pyperclip.copy(image_url)
            if output is True:
                print("\nIt has also been copied to your system clipboard.")
    else:
        upload_success = False
        if output is True:
            print(error_msg)

    return upload_success


if __name__ == "__main__":
    take_screenshot()
