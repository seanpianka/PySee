from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='PySee',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='2.1',

    description='Lightweight Python screenshot tool for Linux and Mac OS X',
    long_description='',

    url='http://pysee.me/',
    author='Sean Pianka',
    author_email='me@seanpianka.com',

    # Choose your license
    license='None',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',

        # Pick your license as you wish (should match "license" above)
        'License :: Free for non-commercial use',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords=['screenshot', 'tool', 'lightweight', 'linux', 'osx', 'mac'],
    install_requires=[
            'imgurpython',
            'zope.interface',
            'pyperclip',
            'clipboard',
            'pytz',
            'datetime',
            'requests'
    ],

    entry_points={
        'console_scripts': [
            'pysee = pysee:_main',
            'pysee-gui = pysee_gui:_main'
        ]
    },
)
