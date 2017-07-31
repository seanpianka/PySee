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
import sys
import errno
from subprocess import Popen, PIPE
from datetime import datetime
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pyperclip

from pysee.hosts import ImageHost
from pysee.exceptions import PySeeError
from pysee.utils import Tool


class PySee:
    TIME_FORMAT = r'%Y-%m-%d-%H-%M-%S'
    DEFAULTS = {'CONFIG_DIR_PATH': os.path.expanduser('~/.config/pysee/'),
                'CONFIG_FILENAME': 'pysee.conf',
                'CONFIG_FILE_CONTENTS': ''}

    def __init__(self, config_dir_path: str="", config_filename: str="", options: dict=None):
        """

        Args:
            config_dir_path:
            config_filename:
            options:
        """
        self.image_host = None

        if not options:
            self.options = {}
        else:
            self.options = options

        self.paths = {'config_dir_path': os.path.expanduser(config_dir_path) if config_dir_path else PySee.DEFAULTS['CONFIG_DIR_PATH'],
                      'config_filename': config_filename if config_filename else PySee.DEFAULTS['CONFIG_FILENAME']}

        self.paths['config_file_path'] = os.path.join(self.paths['config_dir_path'], self.paths['config_filename'])

        # Creates configuration files if not found
        self.config_parser = _setup_configuration_files(self.paths)

        self.paths['images_dir_path'] = os.path.expanduser(
            self.config_parser.get(section='Path', option='default_images_dir_path')
        )

        self.tool = Tool.find_tool_by_name()
        if not self.tool:
            raise PySeeError("No screenshot tool was located on system")

        self.preferred = {
            'mode': self.config_parser.get(section="Preferences", option="mode"),
            'tool': self.config_parser.get(section="Preferences", option="tool")
        }

    @staticmethod
    def _create_configuration_folder(conf_dir_path, conf_filename, conf_file_contents):
        """

        Args:
            conf_dir_path:
            conf_filename:
            conf_file_contents:

        Returns:

        """
        if not os.path.exists(conf_dir_path):
            try:
                print("Creating configuration folder...")
                os.makedirs(conf_dir_path)
            except OSError as e:
                if e.errno != errno.EEXIST or not os.path.isdir():
                    raise PySeeError("Unable to create configuration configuration folder: {}".format(str(e)))

        if not os.path.exists(os.path.join(conf_dir_path, conf_filename)):
            try:
                print("Creating configuration file...")
                with open(conf_dir_path + conf_filename, "w") as f:
                    f.write(conf_file_contents)  # Base configuration file contents
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise PySeeError("Unable to parse configuration file: {}".format(str(e)))

    def run(self, image_host_name, no_clipboard=False, no_output=False,
            no_upload=False, mode="r", timed=0):
        """

        Args:
            image_host_name:
            no_clipboard:
            no_output:
            no_upload:
            mode:
            timed:

        Returns:

        """
        self.image_host = ImageHost.get_image_host_by_name(image_host_name)
        if not self.image_host:
            raise PySeeError("Unable to upload screenshot to selected image host.")

        image_path = self.capture_image(mode)
        image_url = self.upload_image(image_path, no_upload)

        if not no_clipboard:
            pyperclip.copy(image_path if no_upload else image_url)
            if not no_output:
                print("\nIt has also been copied to your system clipboard.")

    def upload_image(self, image_path, no_upload):
        """

        Args:
            image_path:
            no_upload:

        Returns:

        """
        if not no_upload:
            uploaded_image_url = self.image_host.upload(image_path)['link']

            if uploaded_image_url:
                if not no_output:
                    print("Successful upload of {}.png".format(image_path['name']) +
                          "\nYou can find it here: {}".format(response))
            else:
                raise PySeeError("Unable to upload screenshot to selected image host", 2)
        else:
            local_image_path = image_path
            if not no_output:
                print("Successful screenshot! {} was saved locally.".format(local_image_path))

    def capture_image(self, mode: str, extension='png'):
        """

        Args:
            mode:
            extension:

        Returns:

        """
        tool = self.tool
        command = tool.command

        if mode in ["r", "region"]:
            command = ' '.join([command, tool.flags['region']])
        elif mode in ["f", "full"]:
            command = ' '.join([command, tool.flags['full']])
        elif mode in ["w", "window"]:
            command = ' '.join([command, tool.flags['window']])
        else:
            raise PySeeError("No valid screenshot mode selected.")

        current_time = datetime.now().strftime(PySee.TIME_FORMAT)
        image_file_path = ''.join([self.paths['images_dir_path'],
                                  '{}.{} 2>/dev/null'.format(current_time, extension)])
        command = ' '.join([command, tool.flags['filename'], image_file_path])

        try:
            Popen([command], shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE).communicate()
        except:
            raise PySeeError("Failed to process or execute screenshot command", 3)

        return image_file_path


def _setup_configuration_files(paths: dict) -> configparser.ConfigParser:
    """

    Args:
        paths:

    Returns:

    """
    config_parser = configparser.ConfigParser()

    PySee._create_configuration_folder(paths['config_dir_path'],
                                       paths['config_filename'],
                                       PySee.DEFAULTS['CONFIG_FILE_CONTENTS'])

    try:
        config_parser.read(str(paths['config_file_path']))
    except configparser.NoSectionError as e:
        raise PySeeError("Unable to parse configuration file: {}".format(str(e)), 7)

    return config_parser


def _main():
    import argparse

    parser = argparse.ArgumentParser()

    # generate arguments of modes based on supported screenshot modes
    for mode in supported_modes:
        parser.add_argument(
            '--{}'.format(mode),
            '-{}'.format(mode[:1].lower()),
            help='Use the {} mode of an available screenshot \
                  tool to capture an region of the screen.'.format(mode),
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
    args = parser.parse_args()
    no_clipboard = args.no_clipboard
    no_output = args.no_output
    no_upload = args.no_upload
    if not (args.region or args.window or args.full):
        parser.error('No screenshot mode specified,' \
                     ' add --region, --full, or --window')
    else:
        for _mode in supported_modes:
            if getattr(args, _mode):
                mode = _mode
    if not (args.imgur or args.uploads or args.slimg):
        parser.error('No image host specified.')
        sys.exit()
    else:
        for _image_host in supported_hosts:
            if getattr(args, _image_host):
                image_host = _image_host

    app = PySee()
    app.run(no_clipboard=no_clipboard, no_output=no_output,
            no_upload=no_upload, image_host=image_host,
            mode=mode)


if __name__ == "__main__":
    _main()
