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
import argparse
from collections import namedtuple, OrderedDict
from distutils.spawn import find_executable

from error import pysee_errors as pye


def edit_text(filename):
    if os.getenv('EDITOR') is not None:
        os.system("$EDITOR " + filename)
    else:
        try:
            os.system("nano " + filename)
        except:
            os.system("vi " + filename)


def create_tool(name, command, area, window, full, filename):
    # Tool used for creating a namedtuple of available tools
    Tool = namedtuple('Tool', 'name command area window full filename')
    return Tool(name=name, command=command, area=area,
                window=window, full=full, filename=filename)


def is_tool(name):
    return find_executable(name) is not None


def find_screenshot_tool():
    tools = OrderedDict()
    tools['gnome-screenshot'] = create_tool(
            name='gnome-screenshot',
            command='gnome-screenshot -p',
            area='-a',
            window='-w',
            full='',
            filename='-f')
    tools['screencapture'] = create_tool(
            name='screencapture',
            command='screencapture -Cx',
            area='-s',
            window='-w',
            full='',
            filename='')
    tools['shutter'] = create_tool(
            name='shutter',
            command='shutter',
            area='-s',
            window='-w',
            full='-f',
            filename='-o')
    tools['xfce4-screenshooter'] = create_tool(
            name='xfce4-screenshooter',
            command='xfce4-screenshooter',
            area='-r',
            window='-w',
            full='-f',
            filename='-s')
    tools['scrot'] = create_tool(
            name='scrot',
            command='scrot',
            area='-r',
            window='-w',
            full='-f',
            filename='-s')

    for tool in tools:
        if is_tool(tool):
            return tools[tool]


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
        print("There was an error reading the .ini file: ", e)
        sys.exit(4)
