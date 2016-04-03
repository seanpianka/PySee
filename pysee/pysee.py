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

from configs import paths as p, verify_configuration
from helpers import find_screenshot_tool


error_msg = "There was an error when attempting to save" +
            "or upload the screenshot. Please try again."


def capture_screenshot(tool, image_path):
    time_format = r'%Y-%m-%d-%H-%M-%S'

    command = tool.command + ' ' + tool.area + ' ' + tool.filename + ' '
    command += p['imgdir'] + '{}.png 2>/dev/null'
    cmd = Popen([command.format(dt.now().strftime(time_format))], shell=True)
    img_path = p['imgdir'] + dt.now().strftime(time_format) + '.png'
    cmd.communicate()

    img_name = img_path.replace(p['imgdir'], '')[:-4]
    image_path['path'] = img_path # absolute path of screenshot 
    image_path['name'] = img_name # filename of screenshot 


def upload_screenshot(image_host):
    if image_host is "Imgur.com":
        response = imgur.upload_picture(image_path)
        image_url = response['link']
    elif image_host is "Uploads.im":
        img_file = open(image_paths['path'], 'rb')
        response = pass
        image_url = pass

    return {
        'status_code': status_code,
        'image_url': image_url
    }



def take_screenshot(event=None, root=None, image_host="1"):
    verify_configuration()

    tool = find_screenshot_tool()
    image_path = {}

    capture_screenshot(tool, image_path)
    response = upload_screenshot(image_host)

    try:
        if response is None:
            raise requests.exceptions.RequestException
        pyperclip.copy(image_url)
        print("Successful upload of {}.png!".format(image_path['name']),
              "\nYou can find it here: {}".format(image_url),
              "\nIt has also been copied to your system clipboard.")
    except requests.exceptions.RequestException as e:
        print("There was an error: ", e)
        sys.exit(2)
    except:
        print(error_msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
