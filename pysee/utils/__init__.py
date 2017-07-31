"""
utils
~~~~~

Helper functions designed to increase readability
and separate responsbility from the various scripts
used in this project.

:author: Sean Pianka <me@seanpianka.com>
:license: None
"""
import os
from collections import OrderedDict
from distutils.spawn import find_executable


class Tool:
    SUPPORTED_TOOLS = OrderedDict()

    def __init__(self, name, command, region="", window="", full="", filename=""):
        self.name = name
        self.command = command
        self.flags = {'region': region,
                      'window': window,
                      'full': full,
                      'filename': filename}

    @staticmethod
    def find_tool_by_name(tool_name=""):
        for tool in Tool.SUPPORTED_TOOLS:
            if find_executable(tool) and tool == tool_name or not tool_name:
                return Tool.SUPPORTED_TOOLS[tool]

        return None


Tool.SUPPORTED_TOOLS['gnome-screenshot'] = Tool(
    name='gnome-screenshot', command='gnome-screenshot -p', region='-a',
    window='-w', full='', filename='-f'
)
Tool.SUPPORTED_TOOLS['screencapture'] = Tool(
    name='screencapture', command='screencapture -Cx', region='-s',
    window='-w', full='', filename=''
)
Tool.SUPPORTED_TOOLS['shutter'] = Tool(
    name='shutter', command='shutter', region='-s',
    window='-w', full='-f', filename='-o'
)
Tool.SUPPORTED_TOOLS['xfce4-screenshooter'] = Tool(
    name='xfce4-screenshooter', command='xfce4-screenshooter', region='-r',
    window='-w', full='-f', filename='-s'
)
Tool.SUPPORTED_TOOLS['scrot'] = Tool(
    name='scrot', command='scrot', region='-s',
    window='-s', full='', filename=''
)


def edit_text(filename):
    editors = ['gedit', 'nano', 'pico', 'vim', 'vi']

    if os.getenv('EDITOR'):
        editors.insert(0, '$EDITOR')

    for editor in editors:
        if os.system(' '.join([editor, filename])) == 0:
            return

    raise RuntimeError('Unable to open any system text editors.')


# Base location and name of config dir and .conf file
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

