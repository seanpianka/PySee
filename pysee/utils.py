import configparser
import errno
import os

from logger import PySeeLogger


logger = PySeeLogger(__name__)

DEFAULTS = {'CONFIG_DIR_PATH': os.path.expanduser('~/.config/pysee/'),
            'CONFIG_FILENAME': 'pysee.conf',
            'CONFIG_FILE_CONTENTS': '',
            'SAVE_DIR_PATH': os.path.expanduser('~/Pictures/'),
            'TOOL_MODE': 'region',
            'HOST_NAME': 'imgur'}


def get_config_value(section, attr, **kwargs):
    """
    To use:

    >>> get_config_value('Imgur', 'Client-ID')

    Args:
        section:
        attr:
        **kwargs:

    Returns:

    """
    return _get_config_parser(**kwargs)[section][attr]


def _get_config_parser(config_filepath=''):
    """

    Args:
        config_filepath:

    Returns:

    """
    config_parser = None
    if config_filepath == '':
        config_filepath = os.path.join(DEFAULTS['CONFIG_DIR_PATH'],
                                       DEFAULTS['CONFIG_FILENAME'])

    if not os.path.exists(os.path.split(config_filepath)[0]):
        try:
            logger.info("Creating configuration folder...")
            os.makedirs(os.path.split(config_filepath)[0])
        except OSError as e:
            if e.errno != errno.EEXIST or not os.path.isdir():
                logger.exception("Unable to create configuration configuration folder: {}".format(str(e)))
                raise

    if not os.path.exists(config_filepath):
        try:
            logger.info("Creating configuration file...")
            config_parser = configparser.ConfigParser()
            config_parser.add_section('Imgur')
            config_parser.add_section('Slimg')
            config_parser.add_section('Preferences')
            config_parser['Imgur']['client_id'] = ''
            config_parser['Imgur']['client_secret'] = ''
            config_parser['Imgur']['refresh_token'] = ''
            config_parser['Slimg']['client_id'] = ''
            config_parser['Preferences']['tool'] = ''
            config_parser['Preferences']['mode'] = ''

            with open(config_filepath, "w") as f:
                config_parser.write(f)
        except OSError as e:
            if e.errno != errno.EEXIST:
                logger.exception("Unable to parse configuration file: {}".format(str(e)))
                raise

    if not config_parser:
        config_parser = configparser.ConfigParser()
        try:
            config_parser.read(str(config_filepath))
        except configparser.NoSectionError as e:
            logger.exception("Unable to parse configuration file: {}".format(str(e)))
            raise

    return config_parser
