#!/usr/bin/python3
"""
helpers
~~~~~~~

Code provided by http://github.com/imgur/imgurpython examples
Script "helps ease issues between Python 2 and 3"

:author: Jacob Greenleaf <api@imgur.com>

.. seealso:: http://github.com/Imgur/imgurpython/

"""


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
    exit()
