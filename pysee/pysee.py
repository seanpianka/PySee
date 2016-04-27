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
from configs import (paths as p, verify_configuration,
                     supported_hosts, supported_modes)
from helpers import find_screenshot_tool


def process_arguments(parser=None):
    if not parser:
        parser = argparse.ArgumentParser()
    parser.add_argument('--full', "-f", help='', required=False,
                        action="store_true")
    parser.add_argument('--region', "-r", help='', required=False,
                        action="store_true")
    parser.add_argument('--imgur', help='', required=False,
                        action="store_true")
    parser.add_argument('--uploads', help='', required=False,
                        action="store_true")
    parser.add_argument('--window', "-w", help='', required=False,
                        action="store_true")
    parser.add_argument('--no-output', "-o", help='', required=False,
                        action="store_true")
    parser.add_argument('--no-upload', "-u", help='', required=False,
                        action="store_true")
    parser.add_argument('--no-clipboard', "-c", help='', required=False,
                        action="store_true")

    args = parser.parse_args()
    return [args, parser]


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

    try:
        cmd = Popen([command.format(dt.now().strftime(time_format))],
                    shell=True,
                    stdout=PIPE, stdin=PIPE, stderr=PIPE)
        img_path = p['imgdir'] + dt.now().strftime(time_format) + '.png'
        cmd.communicate()

        img_name = img_path.replace(p['imgdir'], '')[:-4]
        image_path['path'] = img_path  # absolute path of screenshot
        image_path['name'] = img_name  # filename of screenshot
        return None
    except:
        return (2, "Failed to process or execute screenshot command")


def upload_screenshot(image_host, image_path):
    try:
        if image_host is "imgur" or image_host is "i":
            response = imgur.upload_picture(image_path)
            if isinstance(response, int) is False:
                return response['link']
            else:
                return response
        elif image_host is "uploads" or image_host is "u":
            response = uploads_im.upload_picture(image_path)
            if isinstance(response, int) is False:
                return response['img_url']
            else:
                return response
        else:
            return 7
    except (KeyboardInterrupt, SystemExit):
        print("Interrupt detected, aborting.\n")
        sys.exit(1)


def take_screenshot(no_clipboard=False, no_output=False, no_upload=False,
                    image_host="i", mode="r"):
    """
    Initializes the process of capturing an area of the screen and saving
    the region to an image file with extension .png.

    Args:
        ~ no_upload: flag which determines if the screenshot should only be
            saved locally or uploaded to image host
        ~ no_clipboard: flag which determines if url from callback will be copied
            to system clipboard
        ~ no_output: flag which determines if log output from tool will be
            displayed in the terminal window
        ~ image_host: determines image host that screenshot will be uploaded to
            expects:
                1) "i" or "imgur" for imgur.com
                2) "s" or "slimg" for sli.mg
                3) "u" or "uploads" for uploads.im
        ~ mode: determines type of screenshot to be taken
            expects:
                1) "r" or "region" for region-select type capture
                2) "f" or "full" for all-monitors type capture
                3) "w" or "window" for window-select type capture
    Returns:
        boolean, if screenshot process was successful
    """
    # Creates configuration files if not found
    verify_configuration()
    # Determines the system's installed screenshot tool
    try:
        screenshot_tool = find_screenshot_tool()
        if screenshot_tool is None:
            raise
    except:
        print("Error: no screenshot tool found.")
        sys.exit()


    # Creation and saving of screenshot + image path to file
    image_path = {}
    capture_screenshot(screenshot_tool, image_path, mode)

    # if the screenshot should be uploaded
    if no_upload is False:
        # response will either be an int (error code) or str (image url)
        response = upload_screenshot(image_host, image_path)
        # if image_url isn't None and isn't an error code
        if None != response and isinstance(response, str):
            if no_output is False:
                print("Successful upload of {}.png!".format(image_path['name']),
                      "\nYou can find it here: {}".format(response))
        elif isinstance(response, int):
            if no_output is False:
                print("Error {}: There was an issue uploading your file to the" +
                      "selected image host.").format(int(response))
                sys.exit(response)
    elif no_upload is True:
        response = image_path['path']
        if no_output is False:
            print("Successful screenshot!" +
                  "{} was saved locally.".format(response))
    if no_clipboard is False:
        # Will copy either system path text or url from response to clipboard
        pyperclip.copy(response)
        if no_output is False:
            print("\nIt has also been copied to your system clipboard.")


if __name__ == "__main__":
    args, parser = process_arguments()
    no_clipboard = args.no_clipboard
    no_output = args.no_output
    no_upload = args.no_upload
    if not (args.region or args.window or args.full):
        parser.error('No screenshot mode specified,' \
                     ' add --region, --full, or --window')
        sys.exit(-3)
    else:
        for _mode in supported_modes:
            if getattr(args, _mode) is True:
                mode = _mode
    if not (args.imgur or args.uploads):
        parser.error('No image host specified,' \
                     ' add --imgur or --uploads')
        sys.exit(-4)
    else:
        for _image_host in supported_hosts:
            if getattr(args, _image_host):
                image_host = _image_host

    take_screenshot(no_clipboard=no_clipboard,
                    no_output=no_output,
                    no_upload=no_upload,
                    image_host=image_host,
                    mode=mode)
