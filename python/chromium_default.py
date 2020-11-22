# -*- coding: utf-8 -*-
# 7.4.0
# 2020-11-21

# Copyright (C) 2018,2019,2020 Brandon Zorn <brandonzorn@cock.li>
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
from pathlib import Path

from python.utils import utils
from python.utils.execute import Execute


class Chrome:
    def __init__(self):
        self.__chrome = None
        self.__chrome_profile = None

        self.__script_name = utils.get_script_name().removeprefix('chromium-')

        self.__display_server = 'x11'
        try:
            if os.environ['WAYLAND_DISPLAY']:
                self.__display_server = 'wayland'
        except KeyError:
            pass

    def start_chrome(self, profile_path):
        Execute(f'{self.__chrome} --user-data-dir={profile_path} --ozone-platform={self.__display_server}')

    def run(self, args):
        if args.chrome == 'chromium':
            self.__chrome = 'chromium'
        elif args.chrome == 'unstable':
            self.__chrome = 'google-chrome-unstable'
        elif args.chrome == 'beta':
            self.__chrome = 'google-chrome-beta'
        else:
            self.__chrome = 'google-chrome'

        # will create temp profile that is deleted after closed
        if args.sandbox or 'sandbox' in self.__script_name:
            from tempfile import TemporaryDirectory
            with TemporaryDirectory() as profile_path:
                self.start_chrome(profile_path=profile_path)
            raise SystemExit

        if args.custom is not None:
            self.__chrome_profile = f'{self.__chrome}-{args.extra}'
        else:
            # script/symlinks must be named chromium-<profile> to work
            # or this can be changed
            # e.g. ln -s chromium-default chromium-<profile>
            self.__chrome_profile = f'{self.__chrome}-{self.__script_name}'

        profile_path = Path() / os.environ['XDG_CONFIG_HOME'] / 'chrome' / self.__chrome_profile

        self.start_chrome(profile_path=profile_path)


def main():
    parser = argparse.ArgumentParser()
    profiles = parser.add_argument_group('PROFILES')
    profiles.add_argument('-C', '--custom',
                          default=None,
                          metavar='PROFILE',
                          help='custom profile, supplied str is used as the profile name')
    profiles.add_argument('-s', '--sandbox',
                          action='store_true',
                          help='sandbox, all data deleted on close, ignores all other profile flags and script name')
    browser = parser.add_argument_group('BROWSER', 'which browser version to use')
    browser.add_argument('-c', '--chrome',
                         default='chromium',
                         metavar='VERSION',
                         choices=['chromium', 'unstable', 'beta', 'release'],
                         help='set specific chrome version to use, [%(choices)s]')
    args = parser.parse_args()

    utils.root_check(require_root=False)

    run = Chrome()
    run.run(args)
