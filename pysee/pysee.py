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
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime as dt

import pyperclip
import imgur

import uploads_im
from error import PySeeError, pysee_errors as pye
from configs import (paths as p, verify_configuration,
                     supported_hosts, supported_modes)
from helpers import find_screenshot_tool, process_arguments


def take_screenshot(no_clipboard=False, no_output=False, no_upload=False,
                    image_host="imgur", mode="r", timed=False):
    """
    Initializes the process of capturing an area of the screen and saving
    the region to an image file with extension .png.

    Args:
        ~ no_upload: flag which determines if the screenshot should only be
            saved locally or uploaded to image host
        ~ no_clipboard: flag which determines if image URL will be copied
            to system clipboard
        ~ no_output: flag which determines if log output from tool will be
            displayed in the terminal window
        ~ image_host: determines image host that screenshot will be uploaded to
            expects:
                1) "imgur" for imgur.com
                2) "slimg" for sli.mg
                3) "uploads" for uploads.im
        ~ mode: determines type of screenshot to be taken
            expects:
                1) "r" or "region" for region-select type capture
                2) "f" or "full" for all-monitors type capture
                3) "w" or "window" for window-select type capture
    Returns:
        boolean, if screenshot process was successful
    """
    # Creates configuration files if not found
    try:
        verify_configuration()
    except PySeeError as e:
        print(e)
        return False

    # Determines the system's installed screenshot tool
    try:
        screenshot_tool = find_screenshot_tool()
        if screenshot_tool is None:
            raise pye['1']
    except PySeeError as e:
        print(e)
        return False

    # Creation and saving of screenshot + image path to file
    try:
        image_path = {}
        capture_screenshot(screenshot_tool, image_path, mode)
    except PySeeError as e:
        print(e)
        return False

    # if the screenshot should be uploaded
    if no_upload is False:
        try:
            response = upload_screenshot(image_host, image_path)
        except PySeeError as e:
            print(e)
            return False
        if response is not None:
            if no_output is False:
                print("Successful upload of {}.png".format(image_path['name']),
                      "\nYou can find it here: {}".format(response))

    elif no_upload is True:
        response = image_path['path'] # absolute path to image
        if no_output is False:
            print("Successful screenshot! \
                   {} was saved locally.".format(response))

    if no_clipboard is False:
        pyperclip.copy(response)
        if no_output is False:
            print("\nIt has also been copied to your system clipboard.")

    return image_path['path']


def capture_screenshot(tool, image_path, mode):
    time_format = r'%Y-%m-%d-%H-%M-%S'

    # Creating the command for which to run based on mode and located tool
    command = tool.command + ' '
    if mode is "r" or mode is "region":
        command += tool.area
    elif mode is "f" or mode is "full":
        command += tool.full
    elif mode is "w" or mode is "window":
        command += tool.window
    command += ' ' + tool.filename + ' ' + p['imgdir'] + '{}.png 2>/dev/null'

    try:
        cmd = Popen([command.format(dt.now().strftime(time_format))],
                    shell=True,
                    stdout=PIPE, stdin=PIPE, stderr=PIPE)
        img_path = p['imgdir'] + dt.now().strftime(time_format) + '.png'
        cmd.communicate()
        img_name = img_path.replace(p['imgdir'], '')[:-4]
        image_path['path'] = img_path  # absolute path of screenshot
        image_path['name'] = img_name  # filename of screenshot
    except:
        raise pye['3']


def upload_screenshot(image_host, image_path):
    try:
        if image_host is "imgur":
            response = imgur.upload_picture(image_path)
            return response['link']
        elif image_host is "uploads":
            response = uploads_im.upload_picture(image_path)
            return response['img_url']
    except PySeeError as e:
        raise(e)


def _main():
    args, parser = process_arguments(supported_hosts, supported_modes)
    no_clipboard = args.no_clipboard
    no_output = args.no_output
    no_upload = args.no_upload
    if not (args.region or args.window or args.full):
        parser.error('No screenshot mode specified,' \
                     ' add --region, --full, or --window')
    else:
        for _mode in supported_modes:
            if getattr(args, _mode) is True:
                mode = _mode
    if not (args.imgur or args.uploads):
        parser.error('No image host specified,' \
                     ' add --imgur or --uploads')
        sys.exit()
    else:
        for _image_host in supported_hosts:
            if getattr(args, _image_host):
                image_host = _image_host

    take_screenshot(no_clipboard=no_clipboard,
                    no_output=no_output,
                    no_upload=no_upload,
                    image_host=image_host,
                    mode=mode)


if __name__ == "__main__":
    _main()
