#!/usr/bin/python
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
import atexit
import argparse
from subprocess import Popen, PIPE, STDOUT

import pyperclip
import imgur
from datetime import datetime as dt

import uploads_im
from configs import paths as p, verify_configuration
from helpers import find_screenshot_tool

error_msg = "There was an error when attempting to save " + \
            "or upload the screenshot. Please try again."


def capture_screenshot(tool, image_path, mode):
    time_format = r'%Y-%m-%d-%H-%M-%S'

    # Creating the command for which to run based on mode and located tool
    command = tool.command + ' '
    if mode is "r" or mode is "region":
        command += tool.area
    elif mode is "f" or mode is "full":
        command += tool.full
    elif mode is "w" or mode is "window":
        command =+ tool.window
    command += ' ' + tool.filename + ' ' + p['imgdir'] + '{}.png 2>/dev/null'

    cmd = Popen([command.format(dt.now().strftime(time_format))],
                shell=True,
                stdout=PIPE, stdin=PIPE, stderr=PIPE)
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
            image_url = None

        return image_url
    except (KeyboardInterrupt, SystemExit):
        print("Interrupt detected, aborting.\n")
        return None


def take_screenshot(clipboard=True, output=True,
                    image_host="i", mode="r"):
    """
    Initializes the process of capturing an area of the screen and saving
    the region to an image file with extension .png.

    Args:
        clipboard: flag which determines if url from callback will be copied
                   to system clipboard
        output: flag which determines if log output from tool will be
                displayed in the terminal window
        image_host: determines image host that screenshot will be uploaded to
            expects:
                1) "i" or "imgur" for imgur.com
                2) "s" or "slimg" for sli.mg
                3) "u" or "uploads" for uploads.im
        mode: determines type of screenshot to be taken
            expects:
                1) "r" or "region" for region-select type capture
                2) "f" or "full" for all-monitors type capture
                3) "w" or "window" for window-select type capture
    Returns:
        boolean, if screenshot process was successful
    """
    verify_configuration()

    screenshot_tool = find_screenshot_tool()
    image_path = {}
    capture_screenshot(screenshot_tool, image_path)
    image_url = upload_screenshot(image_host, image_path)

    if image_url is not None and image_url is not "":
        if image_url is None:
            if output is True:
                print("Successful screenshot!" +
                      "{} was saved locally.".format(image_path['path']))
            image_url = image_path['path']
        else:
            if output is True:
                print("Successful upload of {}.png!".format(image_path['name']),
                      "\nYou can find it here: {}".format(image_url))
            upload_status = True
        if clipboard is True:
            pyperclip.copy(image_url)
            if output is True:
                print("\nIt has also been copied to your system clipboard.")
    else:
        upload_status = False
        if output is True:
            print(error_msg)

    return upload_status


if __name__ == "__main__":
    take_screenshot()
