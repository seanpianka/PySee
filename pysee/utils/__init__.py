"""
helpers
~~~~~~~

Helper functions designed to increase readability
and separate responsbility from the various scripts
used in this project.

:author: Sean Pianka <me@seanpianka.com>
:license: None
"""
import os
import sys
import errno
import argparse
import configparser
from collections import OrderedDict
from distutils.spawn import find_executable


class Tool:
    def __init__(self, name, command, area="", window="", full="", filename=""):
        self.name = name
        self.command = command
        self.flags = {
            'area': area,
            'window': window,
            'full': full,
            'filename': filename
        }


tools = OrderedDict()
tools['gnome-screenshot'] = Tool(name='gnome-screenshot',
                                 command='gnome-screenshot -p',
                                 area='-a',
                                 window='-w',
                                 full='',
                                 filename='-f')
tools['screencapture'] = Tool(name='screencapture',
                              command='screencapture -Cx',
                              area='-s',
                              window='-w',
                              full='',
                              filename='')
tools['shutter'] = Tool(name='shutter',
                        command='shutter',
                        area='-s',
                        window='-w',
                        full='-f',
                        filename='-o')
tools['xfce4-screenshooter'] = Tool(name='xfce4-screenshooter',
                                    command='xfce4-screenshooter',
                                    area='-r',
                                    window='-w',
                                    full='-f',
                                    filename='-s')
tools['scrot'] = Tool(name='scrot',
                      command='scrot',
                      area='-s',
                      window='-s',
                      full='',
                      filename='')


def edit_text(filename):
    editors = ['gedit', 'nano', 'pico', 'vim', 'vi']

    if os.getenv('EDITOR') is not None:
        editors.insert(0, '$EDITOR')

    for editor in editors:
        if os.system(' '.join([editor, filename])) == 0:
            break
    else:
        raise RuntimeError('Unable to open any system text editors.')


def find_screenshot_tool(desired_tool_name=""):
    for tool_name in tools:
        if find_executable(tool_name) is not None:
            if desired_tool_name == "":
                return tools[tool_name]
            elif desired_tool_name == tool_name:
                return tools[tool_name]

    return None


def process_arguments(supported_hosts, supported_modes, parser=None):
    if not parser:
        parser = argparse.ArgumentParser()

    # generate arguments of modes based on supported screenshot modes
    for mode in supported_modes:
        parser.add_argument(
            '--{}'.format(mode),
            '-{}'.format(mode[:1].lower()),
            help='Use the {} mode of an available screenshot \
                  tool to capture an area of the screen.'.format(mode),
            action="store_true")
    # generate arguments of hosts based on supported image host
    for host in supported_hosts:
        # ensuring image host flags will not conflict with mode flags
        short_flag = '-{}'.format(host[:1].lower()) \
                     if '-{}'.format(host[:1].lower()) not in ['w','r','f'] \
                     else '-{}'.format(host[:2].lower())
        parser.add_argument(
            '--{}'.format(host),
            short_flag,
            help='Upload screenshot to {}'.format(host),
            action="store_true")

    parser.add_argument('--no-upload', "-1",
                        help='Do not upload to an image host \
                              (does not conflict with image host flags)',
                        action="store_true")
    parser.add_argument('--no-output', "-2",
                        help='Surpress output from the scripts',
                        action="store_true")
    parser.add_argument('--no-clipboard', "-3",
                        help='Prevents copying of returned \
                              image URL to the system clipboard',
                        action="store_true")
    parser.add_argument('--timed', "-4",
                        help='Allows screenshots to occur automatically \
                              at a set time interval on a specific screen \
                              region',
                        action="store_true")
    return [parser.parse_args(), parser]


def get_config():
    '''Create a config parser for reading INI files'''
    try:
        import ConfigParser
        return ConfigParser.ConfigParser()
    except:
        import configparser
        return configparser.ConfigParser()


def init_config(path):
    config = get_config()
    try:
        config.read(path)
        return config
    except helpers.ConfigParser.NoSectionError as e:
        print("There was an error reading the settings file: ", e)
        sys.exit()

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
from error import pysee_errors as pye

# Known hosts lists, used when checking for arguments
supported_hosts = ['imgur', 'uploads', 'slimg']
supported_modes = ['region', 'window', 'full']

# Base location and name of config dir and .conf file
paths = {}
config_file_name = 'pysee.conf'
paths['config_dir_path'] = os.path.expanduser('~/.config/pysee/')
paths['config_file_name'] = config_file_name
base_config_file_contents = """[Imgur_API]
client_id=65701d960c6ab14
client_secret=YOUR_SECRET_HERE
refresh_token=

[Slimg_API]
client_id=eIVbKCqD3Omkiv0gADKyj6adX74QYhYc
client_secret=YOUR_SECRET_HERE

[path]
config_dir_path=~/.config/pysee/
base_img_path=~/Pictures/"""


def verify_configuration():
    conf_dir_path = paths['config_dir_path']
    conf_file = paths['config_file_name']

    if os.path.exists(conf_dir_path) is False:
        try:
            print("Creating configuration folder...")
            os.makedirs(conf_dir_path)
        except OSError as e:
            if e.errno != errno.EEXIST or not os.path.isdir():
                raise pye['7']

    if os.path.exists(conf_dir_path + conf_file) is False:
        try:
            print("Creating configuration file...")
            with open(conf_dir_path + conf_file, "w") as f:
                f.write(base_config_file_contents)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise pye['7']

    config_parser = init_config(conf_dir_path + conf_file)
    paths['imgdir'] = os.path.expanduser(config_parser.get('path', 'base_img_path'))

    try:
        pyperclip.copy('0')
    except pyperclip.exceptions.PyperclipException:
        raise pye['5']


if __name__ == "__main__":
    verify_configuration()
