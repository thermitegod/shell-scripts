# -*- coding: utf-8 -*-
# 8.5.0
# 2021-04-29

# Copyright (C) 2018,2019,2020,2021 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

import argparse
import os
import sys
from pathlib import Path

from loguru import logger

from python.utils.check_env import CheckEnv
from python.utils.execute import Execute
from python.utils.root_check import RootCheck


class Chrome:
    def __init__(self, args: argparse = None):
        self.__chrome = None
        self.__chrome_profile = None

        self.__profile_name = CheckEnv.get_script_name().removeprefix('chromium-')

        self.__display_server = 'x11'
        try:
            if os.environ['WAYLAND_DISPLAY']:
                self.__display_server = 'wayland'
        except KeyError:
            pass

        self.run(args=args)

    def start_chrome(self, profile_path):
        Execute(f'{self.__chrome} '
                f'--user-data-dir={profile_path}  '
                f'--ozone-platform={self.__display_server} '
                f'--no-default-browser-check')

    def run(self, args):
        if args.chrome == 'chromium':
            self.__chrome = 'chromium'
        elif args.chrome == 'unstable':
            self.__chrome = 'google-chrome-unstable'
        elif args.chrome == 'beta':
            self.__chrome = 'google-chrome-beta'
        else:
            self.__chrome = 'google-chrome'

        if args.custom:
            self.__chrome_profile = f'{self.__chrome}-{args.extra}'
        else:
            # script/symlinks must be named chromium-<profile> to work
            # or this can be changed
            # e.g. ln -s chromium-default chromium-<profile>
            self.__chrome_profile = f'{self.__chrome}-{self.__profile_name}'

        profile_path = Path() / os.environ['XDG_CONFIG_HOME'] / 'chrome' / self.__chrome_profile

        self.start_chrome(profile_path=profile_path)


def main():
    parser = argparse.ArgumentParser()
    profiles = parser.add_argument_group('profiles')
    profiles.add_argument('-C', '--custom',
                          default=None,
                          metavar='PROFILE',
                          help='custom profile, supplied str is used as the profile name')
    browser = parser.add_argument_group('browser', 'which browser version to use')
    browser.add_argument('-c', '--chrome',
                         default='unstable',
                         metavar='VERSION',
                         choices=['chromium', 'unstable', 'beta', 'release'],
                         help='set specific chrome version to use, [%(choices)s]')
    debug = parser.add_argument_group('debug')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    RootCheck(require_root=False)

    Chrome(args=args)
