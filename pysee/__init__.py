"""
PySee
~~~~~
A lightweight screenshot tool with automatic
Imgur uploading and system clipboard copying.

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None

"""
import logging
import os
import sys
import copy
from datetime import datetime
from subprocess import Popen, PIPE
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pyperclip

from hosts import HOSTS
from tools import CaptureTool
from logger import PySeeLogger
from utils import DEFAULTS


__author__ = 'Sean Pianka'
__email__ = 'pianka@eml.cc'
__version__ = '2.0.0'

logger = PySeeLogger(__name__)


def run(host_name=DEFAULTS['HOST_NAME'], tool_name=None, no_clipboard=False,
        no_output=False, no_upload=False, mode=DEFAULTS['TOOL_MODE'],
        save_dir=DEFAULTS['SAVE_DIR_PATH'], title='', timed=0, delay=0):
    """

    Args:
        host_name:
        tool_name:
        no_clipboard:
        no_output:
        no_upload:
        mode:
        save_dir:
        title:
        timed:
        delay:

    Returns:

    """
    if no_output:
        logging.propagate = False

    # Logic for finding valid installed tool uses popitem, must restore list...
    valid_tools_tmp = copy.copy(CaptureTool.valid_tools)

    try:
        tool_name = tool_name.lower()
        tool = CaptureTool.valid_tools[tool_name]
    except (IndexError, AttributeError):
        logger.debug('Invalid tool name provided.')
        tool = None
        while not tool:
            try:
                tool_name, tool = CaptureTool.valid_tools.popitem()
                if tool.modes[mode] == '':
                    logger.debug('Found installed tool, but lacked support for desired mode.')
                    tool = None
            except KeyError:
                err = "No installed tool supports the mode \"{}\".".format(mode)
                logger.exception(err)
                raise LookupError(err)

    # Restoring list, eventually will fix crummy logic above...
    CaptureTool.valid_tools = valid_tools_tmp

    try:
        host = HOSTS[host_name]
        host_name = host_name.lower()
    except KeyError:
        logger.debug('Invalid host name provided.')
        host = HOSTS[DEFAULTS['HOST_NAME']]

    try:
        image_filepath = take_screenshot(tool, mode, save_dir, title=title)
    except KeyboardInterrupt:
        sys.exit()
    logger.info('Screenshot capture: "{}" was saved in "{}".'.format(os.path.split(image_filepath)[-1], save_dir))
    if not no_upload:
        image_url = upload_screenshot(image_filepath, host, title)
        logger.info('Image upload: "{}" was uploaded to "{}" at "{}".'.format(os.path.split(image_filepath)[-1], host_name, image_url))
    else:
        image_url = image_filepath

    if not no_clipboard:
        pyperclip.copy(image_url)
        logger.info('Clipboard copy: "{}" has been copied to your system clipboard.'.format(image_url))

    logging.propagate = True

    return image_url


def take_screenshot(tool, mode, save_dir, title='', extension='png'):
    """ Execute the CaptureTool instance for whichever screenshotting tool with
    the provided screenshot mode, and save the new screenshot to the filename
    and extension specified.

    Args:
        tool: a CaptureTool instance
        mode: an element of Capturetool.valid_modes, modes for screenshot tool
        save_dir: where to save the screenshot
        title: save picture with title
        extension: save picture with extension

    Returns: absolute filepath to the screenshot

    """
    time_format = r'%Y-%m-%d-%H-%M-%S'

    if not isinstance(tool, CaptureTool):
        err = "Provided capture tool must be a CaptureTool instance."
        logger.error(err)
        raise TypeError(err)

    if mode not in CaptureTool.valid_modes:
        err = "Invalid screenshot mode provided."
        logger.error(err)
        raise LookupError(err)
    if mode not in tool.modes.keys():
        err = "Provided tool does not support the desired mode."
        logger.error(err)
        raise AttributeError("Provided tool does not support the desired mode.")

    current_time = datetime.now().strftime(time_format)
    if '' == title:
        title = ('.'.join([current_time, extension]))
    image_filepath = os.path.join(os.path.abspath(save_dir), title)

    try:
        command = ' '.join([tool.command,
                            tool.modes[mode],
                            tool.flags.get('filename', ''),
                            image_filepath])
    except KeyError:
        err = "Selected tool does not support the desired mode."
        logger.error(err)
        raise LookupError(err)

    cmd = Popen([command], shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    try:
        stdout, stderr = cmd.communicate()
        ret = cmd.wait()

        if ret != 0:
            err = "Screenshot tool process exited with a non-zero return code ({}): stdout: \"{}\"; stderr: \"{}\"".format(ret, stdout, stderr)
            logger.error(err)
            raise RuntimeError(err)
    except KeyboardInterrupt:
        err = "Screenshot tool process was exited before the screenshot completed."
        logger.error(err)
        raise KeyboardInterrupt(err)

    return image_filepath


def upload_screenshot(image_path, host_upload, title):
    """ Upload a screenshot given an image API function and title.

    Args:
        image_path: path to screenshot file to be uploaded
        host_upload: a CaptureTool instance indicating which screenshot tool to use
        title: title of the screenshot to be provided to the image API

    """
    if not callable(host_upload):
        err = "Provided image host must be a `host_upload` function instance."
        logger.error(err)
        raise TypeError(err)

    response = host_upload(image_path, title)
    if not response:
        err = "Image upload failed."
        logger.error(err)
        raise RuntimeError(err)

    logger.debug("Image upload succeeded.")
    return response


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', '-m', metavar='mode', type=str, default=DEFAULTS['TOOL_MODE'],
                        help='Set the mode to take a screenshot in. Ensure you \
                        have a screenshot tool installed which supports the \
                        desired mode.')

    parser.add_argument('--image-host', '-i', metavar='host', type=str, default=DEFAULTS['HOST_NAME'],
                        help='Image host name to upload the screenshot to.', action="store", dest="host_name")

    parser.add_argument('--screenshot-tool', '-s', metavar='tool', type=str,
                        help='Name of screenshot program to use.', action="store", dest="tool_name")

    parser.add_argument('--save-directory', '-d', metavar='dir', type=str, default=DEFAULTS['SAVE_DIR_PATH'],
                        help='Where to locally save the screenshot.', action="store", dest="save_dir")

    parser.add_argument('--title', '-t', metavar='name', type=str,
                        help='Give the screenshot a custom title.')

    parser.add_argument('--no-upload', "-u", default=False,
                        help='Do not upload to an image host.',
                        action="store_true")

    parser.add_argument('--no-output', "-o", default=False,
                        help='Do not output any logged information.',
                        action="store_true")

    parser.add_argument('--no-clipboard', "-c", default=False,
                        help='Do not copy image URL to system clipboard.',
                        action="store_true")

    parser.add_argument('--delay', metavar='N', type=int, default=0,
                        help='Set a delay of `N` seconds before taking the screenshot. \
                              Ensure you have a screenshot tool installed which \
                              supports this feature.')

    parser.add_argument('--timed', metavar='N', type=int, default=0,
                        help='Allows screenshots to occur automatically \
                              every `N` seconds on a specific screen \
                              region until the program has exited.')

    args = vars(parser.parse_args())
    args['mode'] = args['mode'].lower()

    if args['mode'] not in CaptureTool.valid_modes:
        parser.error('No screenshot mode specified; add --mode [region,full,window].')

    # Remove None objects from dictionary.
    args = {k: v for k, v in args.items() if v is not None}

    try:
        run(**args)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
