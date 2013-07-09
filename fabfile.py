#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import os

from fabric.api import local


SETTINGS = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wlan_simulation_game.global_settings import *

SECRET_KEY= %(secret_key)r
"""


def settings():
    """
    Creates local settings file.
    """
    if os.path.exists('settings.py'):
        print 'Settings file already exists.'
    else:
        with open('settings.py', 'wb') as settings_file:
            settings_file.write(SETTINGS % {'secret_key': base64.b64encode(os.urandom(30))})
        print 'Settings file successfully created.'
