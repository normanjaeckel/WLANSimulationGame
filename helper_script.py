#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import base64
import os

from wlan_simulation_game import __version__ as wlan_simulation_game_version


SETTINGS = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wlan_simulation_game.global_settings import *

SECRET_KEY = %(secret_key)r

# If you have problems, uncomment the next two lines to run the server in debug mode.
# DEBUG = True
# TEMPLATE_DEBUG = DEBUG
"""


def main():
    args = parse_args()
    if args.create_settings:
        create_settings()
    elif args.pep8:
        pep8()
    else:
        print 'Use --help for more details.'
    return 0


def parse_args():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(description='WLAN Simulation Game Helper Script')
    parser.add_argument(
        '--create-settings',
        action='store_true',
        help='Create local settings file.')
    parser.add_argument(
        '--pep8',
        action='store_true',
        help='Check for pep8 errors.')
    parser.add_argument(
        '--version',
        action='version',
        version=wlan_simulation_game_version,
        help='Show version number and exit.')
    return parser.parse_args()


def create_settings():
    """
    Creates local settings file.
    """
    if os.path.exists('settings.py'):
        print 'Settings file already exists.'
    else:
        with open('settings.py', 'wb') as settings_file:
            settings_file.write(SETTINGS % {'secret_key': base64.b64encode(os.urandom(30))})
        print 'Settings file successfully created.'


def pep8():
    """
    Checks for PEP 8 errors.
    """
    try:
        import pep8
    except ImportError:
        print 'Pep8 (Python style guide checker) is not installed. Try pip install pep8.'
    else:
        pep8style = pep8.StyleGuide(max_line_length=150)
        pep8style.input_dir('wlan_simulation_game')
        print 'Style guide check finished.'


if __name__ == '__main__':
    main()
