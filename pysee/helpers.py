#!/usr/bin/python3
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
from collections import namedtuple, OrderedDict
from distutils.spawn import find_executable


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
    tools['gnome-screenshot'] = create_tool(name='gnome-screenshot',
                                            command='gnome-screenshot -p',
                                            area='-a',
                                            window='-w',
                                            full='',
                                            filename='-f')
    tools['screencapture'] = create_tool(name='screencapture',
                                         command='screencapture -Cx',
                                         area='-s',
                                         window='-w',
                                         full='',
                                         filename='')
    tools['shutter'] = create_tool(name='shutter',
                                   command='shutter',
                                   area='-s',
                                   window='-w',
                                   full='-f',
                                   filename='-o')
    for tool in tools:
        if is_tool(tool):
            return tools[tool]


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
        exit()

if __name__ == "__main__":
    pass
