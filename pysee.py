"""
PySee
~~~~~
A lightweight screenshot tool with automatic
Imgur uploading and system clipboard copying.

:author: Sean Pianka <me@seanpianka.com>
:copyright: Copyright 2016 Sean Pianka
:license: None

"""
import argparse
import configparser
import errno
import os
import logging as _logging
import sys
import copy
from distutils.spawn import find_executable
from datetime import datetime
from subprocess import Popen, PIPE
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import imgurpython
import requests
import pyperclip

__author__ = 'Sean Pianka'
__email__ = 'pianka@eml.cc'
__version__ = '2.0.0'


DEFAULTS = {'CONFIG_PATH': os.path.expanduser('~/.config/pysee/pysee.conf'),
            'SAVE_DIR': os.path.expanduser('~/Pictures/'),
            'MODE': 'region',
            'CLIPBOARD': True,
            'UPLOAD': True,
            'LOGGING': True,
            'SAVE': True}


class PySee:
    def __init__(self, init=False):
        self.cp = PySeeConfigParser()

        if init:
            self.init_config()

        if not os.path.exists(DEFAULTS['CONFIG_PATH']):
            raise configparser.ParsingError("Unable to parse configuration file, please run \"pysee --init\".")

        self.cp.read(DEFAULTS['CONFIG_PATH'])

        # Update DEFAULTS with user specified preferences
        for k, v in DEFAULTS.items():
            try:
                DEFAULTS[k] = self.cp.get_val('Preferences', k, boolean=type(v)==bool)
            except configparser.ParsingError as e:
                DEFAULTS[k] = v

    def init_config(self):
        print("This utility will walk you through creating your PySee configuration file.")
        print("It will cover each required setting and tries to provide sensible defaults.\n")
        print("PySee's configuration file will be stored at \"~/.config/pysee/pysee.conf\".\n")
        print("Press ^C at any time to quit.")

        try:
            values = {}
            values["TOOL"] = input("Screenshot capture tool [{}]: ({}) ".format('|'.join(CaptureTool.valid_tools.keys()), DEFAULTS['TOOL'])).lower()
            values['HOST'] = input("Image host [{}]: ({}) ".format('|'.join(ImageHost.valid_hosts.keys()), DEFAULTS['HOST'])).lower()
            values["MODE"] = input("Capture mode [region|full|window]: (region) ").lower()
            values["SAVE_DIR"] = input("Screenshot save directory: ({}) ".format(DEFAULTS['SAVE_DIR']))
            values["CLIPBOARD"] = input("Copy uploaded URL to clipboard: (yes) ")
            values["UPLOAD"] = input("Upload screenshot after capture: (yes) ")
            values["LOGGING"] = input("Print logging information: (yes) ")
            values["SAVE"] = input("Save screenshot locally after capture: (yes) ")
            values["IMGUR_CLIENT_ID"] = input("Imgur API Client ID (http://api.imgur.com/oauth2/addclient): ('') ")
            values["IMGUR_CLIENT_SECRET"] = input("Imgur API Client Secret: ('') ")
        except KeyboardInterrupt:
            sys.exit()

        self.cp.update_config(values)
        self.cp.write_config()

    def main(self, host_name, tool_name, mode, clipboard, logging, upload, save, save_dir):
        if not logging:
            _logging.propagate = False

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
            host = ImageHost.valid_hosts[host_name]
            host_name = host_name.lower()
        except KeyError:
            logger.debug('Invalid host name provided.')
            host = ImageHost.valid_hosts[DEFAULTS['HOST_NAME']]

        image_filepath = self.take_screenshot(tool, mode, save_dir)
        logger.info('Screenshot capture: "{}" was saved in "{}".'.format(os.path.split(image_filepath)[-1], save_dir))
        if upload:
            image_url = self.upload_screenshot(image_filepath, host)
            logger.info('Image upload: "{}" was uploaded to "{}" at "{}".'.format(os.path.split(image_filepath)[-1], host_name, image_url))
        else:
            image_url = image_filepath

        if clipboard:
            pyperclip.copy(image_url)
            logger.info('Clipboard copy: "{}" has been copied to your system clipboard.'.format(image_url))

        if not save:
            os.remove(image_filepath)

        _logging.propagate = True

        return image_url

    def take_screenshot(self, tool, mode, save_dir, extension='png'):
        """ Execute the CaptureTool instance for whichever screenshotting tool with
        the provided screenshot mode, and save the new screenshot to the filename
        and extension specified.

        Args:
            tool: a CaptureTool instance
            mode: an element of Capturetool.valid_modes, modes for screenshot tool
            save_dir: where to save the screenshot
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

        image_filepath = os.path.join(os.path.abspath(save_dir), '.'.join([current_time, extension]))

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

    def upload_screenshot(self, image_path, image_host):
        """ Upload a screenshot given an image API function.

        Args:
            image_path: path to screenshot file to be uploaded
            host_upload: a CaptureTool instance indicating which screenshot tool to use
            **kwargs: lambdas to

        """
        if not isinstance(image_host, ImageHost):
            err = "Provided image_host must be a ImageHost instance."
            logger.error(err)
            raise TypeError(err)

        response = image_host.upload(image_path, self.cp)
        if not response:
            err = "Image upload failed."
            logger.error(err)
            raise RuntimeError(err)

        logger.debug("Image upload succeeded.")
        return response


class PySeeConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        configparser.ConfigParser.__init__(self, *args, **kwargs)

    def read_config(self, filename):
        self.read(filename)

        if not os.path.exists(os.path.split(filename)[0]) or not os.path.exists(filename) or not self.sections():
            raise configparser.ParsingError("Unable to parse configuration file, please run \"pysee --init\".")

    def update_config(self, values=None):
        try:
            self.add_section('Imgur')
            self['Imgur']['client_id'] = values.get("IMGUR_CLIENT_ID", '')
            self['Imgur']['client_secret'] = values.get("IMGUR_CLIENT_SECRET", '')
        except configparser.DuplicateSectionError:
            pass

        try:
            self.add_section('Preferences')
        except configparser.DuplicateSectionError:
            pass
        self['Preferences']["CONFIG_PATH"] = os.path.expanduser(DEFAULTS['CONFIG_PATH'])
        self['Preferences']["TOOL"] = values['TOOL'] if values.get('TOOL') in CaptureTool.valid_tools else DEFAULTS['TOOL']
        self['Preferences']["HOST"] = values['HOST'] if values.get('HOST') in ImageHost.valid_hosts else DEFAULTS['HOST']
        self['Preferences']["MODE"] = values['MODE'] if values.get('MODE') in CaptureTool.valid_modes else DEFAULTS['MODE']
        self['Preferences']["SAVE_DIR"] = values["SAVE_DIR"] or DEFAULTS["SAVE_DIR"]

        for key in ["CLIPBOARD", "UPLOAD", "LOGGING", "SAVE"]:
            test = str(values.get(key, '')).lower()
            if test in ("yes", "y", "true", "1"):
                self['Preferences'][key] = "1"
            elif test in ("no", "n", "false", "0"):
                self['Preferences'][key] = "0"
            else:
                self['Preferences'][key] = str(DEFAULTS[key]).lower()

        # Update DEFAULTS with user specified preferences
        for k, v in DEFAULTS.items():
            try:
                DEFAULTS[k] = self.get_val('Preferences', k, boolean=type(v)==bool)
            except configparser.ParsingError as e:
                DEFAULTS[k] = v

    def write_config(self):
        try:
            os.makedirs(os.path.dirname(self['Preferences']['CONFIG_PATH']))
        except FileExistsError:
            pass

        with open(self['Preferences']['CONFIG_PATH'], "w") as f:
            self.write(f)

    def get_val(self, section, attr, boolean=None):
        if boolean:
            return self.getboolean(section, attr)
        return self[section][attr]

    def set_val(section, attr, value):
        self[section][attr] = str(value).lower() if type(value) == bool else str(value)


class CaptureTool:
    valid_tools = {}
    valid_modes = ['region', 'full', 'window']
    valid_flags = ['filename']

    def __init__(self, name, command, **kwargs):
        self.name = name
        self.command = command
        self.modes = {mode: kwargs.get(mode, '')
                      for mode in CaptureTool.valid_modes}
        self.flags = {flag: kwargs.get(flag, '')
                      for flag in CaptureTool.valid_flags}

        # CaptureTool is not valid if not installed.
        if find_executable(name): CaptureTool.valid_tools[name] = self


class ImageHost:
    valid_hosts = {}

    def __init__(self, name, upload, **kwargs):
        if not callable(upload):
            raise ValueError('upload_function must be callable.')

        self.name = name
        self.upload = lambda image_path, cp: upload(image_path, cp)
        ImageHost.valid_hosts[name] = self

    @staticmethod
    def _imgur_upload(image_path, cp):
        client = imgurpython.ImgurClient(cp.get_val('Imgur', 'client_id'), cp.get_val('Imgur', 'client_secret'))

        try:
            config = { 'name': os.path.split(image_path)[-1],
                      'description': 'Screenshot taken via PySee'}

            response = client.upload_from_path(image_path, config=config, anon=True)
            logger.debug("Imgur upload via imgurpython was successful.")
            return response['link']
        except imgurpython.helpers.error.ImgurClientError:
            logger.exception("There was an error validating your API keys for imgur.com.\n" +
                              "Go to https://api.imgur.com/oauth2/addclient to receive your" +
                              " own API keys.\n")
            raise

class PySeeFormatter(_logging.Formatter):
    err_fmt  = "[*] ERROR: %(msg)s"
    dbg_fmt  = "[-] DEBUG: %(module)s: %(lineno)d: %(msg)s"
    info_fmt = "[+] %(msg)s"

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by _logging level
        if record.levelno == _logging.DEBUG:
            self._style._fmt = PySeeFormatter.dbg_fmt

        elif record.levelno == _logging.INFO:
            self._style._fmt = PySeeFormatter.info_fmt

        elif record.levelno == _logging.ERROR:
            self._style._fmt = PySeeFormatter.err_fmt

        # Call the original formatter class to do the grunt work
        result = _logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


class PySeeLogger(_logging.Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        formatter = PySeeFormatter()
        handler = _logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.setLevel(_logging.INFO)


logger = PySeeLogger(__name__)
_logging.getLogger("requests").setLevel(_logging.WARNING)

CaptureTool('gnome-screenshot', 'gnome-screenshot', region='-a', window='-w', filename='-f')
CaptureTool('screencapture', 'screencapture -Cx', region='-s', window='-w')
CaptureTool('shutter', 'shutter', region='-s', window='-w', full='-f', filename='-o')
CaptureTool('xfce4-screenshooter', 'xfce4-screenshooter', region='-r', window='-w', full='-f', filename='-s')
CaptureTool('scrot', 'scrot', region='-s', window='-s', full=' ')
DEFAULTS['TOOL'] = list(CaptureTool.valid_tools.keys())[0]

ImageHost('imgur', ImageHost._imgur_upload)
DEFAULTS['HOST'] = list(ImageHost.valid_hosts.keys())[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--init', default=False,
                        help='Initialize PySee and its configuration file information.',
                        action="store_true")

    parser.add_argument('--mode', '-m', metavar='mode', type=str, default=DEFAULTS['MODE'],
                        help='Set the mode to take a screenshot in. Ensure you \
                        have a screenshot tool installed which supports the \
                        desired mode.')

    parser.add_argument('--image-host', '-i', metavar='host', type=str, default=DEFAULTS['HOST'],
                        help='Image host name to upload the screenshot to.', action="store", dest="host_name")

    parser.add_argument('--screenshot-tool', '-t', metavar='tool', type=str, default=DEFAULTS['TOOL'],
                        help='Name of screenshot program to use.', action="store", dest="tool_name")

    parser.add_argument('--save-directory', '-d', metavar='dir', type=str, default=DEFAULTS['SAVE_DIR'],
                        help='Where to locally save the screenshot.', action="store", dest="save_dir")

    parser.add_argument('--upload', "-u", default=DEFAULTS['UPLOAD'],
                        help='Upload screenshot to an image host after capture.',
                        action="store_true")

    parser.add_argument('--logging', "-l", default=DEFAULTS['LOGGING'],
                        help='Output any logged information to the terminal.',
                        action="store_true")

    parser.add_argument('--clipboard', "-c", default=DEFAULTS['CLIPBOARD'],
                        help='Copy image URL to system clipboard after capture.',
                        action="store_true")

    parser.add_argument('--save', "-s", default=DEFAULTS['SAVE'],
                        help='Save screenshot locally after capture.',
                        action="store_true")

    parser.add_argument('--gui', default=False,
                        help='Start PySee in GUI mode.',
                        action="store_true")

    args = {k: v for k, v in vars(parser.parse_args()).items() if v is not None}
    args['mode'] = args['mode'].lower()

    if args['mode'] not in CaptureTool.valid_modes:
        parser.error('Invalid capture mode specified [region,full,window].')

    if args['init']:
        pysee = PySee(init=True)
        print("PySee is ready to use!")
        sys.exit()

    pysee = PySee()

    if args['gui']:
        import gui as gui
        gui.main()
    else:
        try:
            del args['init']
            del args['gui']
            pysee.main(**args)
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
