#!/usr/bin/env python3
# 1.4.0
# 2020-12-03

# Copyright (C) 2020 Brandon Zorn <brandonzorn@cock.li>
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

from python.utils.check_env import CheckEnv
from python.utils.execute import Execute


class Symlink:
    def __init__(self):
        # since root is req to do this Path.home() will return
        # /root so create wanted home path
        self.__user = 'brandon'

        self.__home = Path() / '/home' / self.__user
        self.__local_bin = Path() / '/usr/local/bin'

        self.__ignore = '--ignore=".git" ' \
                        '--ignore=".idea" ' \
                        '--ignore=".gitignore" ' \
                        '--ignore="deprecated" ' \
                        '--ignore="python" ' \
                        '--ignore="shell" ' \
                        '--ignore="tools" ' \
                        '--ignore="utils" '

    def run(self, args):
        if args.stow_bin:
            os.chdir(self.__home)
            Execute(f'stow {self.__ignore} -v --target={self.__local_bin} .bin')
        if args.unstow_bin:
            os.chdir(self.__home)
            Execute(f'stow {self.__ignore} -D -v --target={self.__local_bin} .bin')


def main():
    parser = argparse.ArgumentParser()
    stow = parser.add_argument_group('STOW')
    stow.add_argument('-b', '--stow-bin',
                      action='store_true',
                      help='')
    unstow = parser.add_argument_group('UNSTOW')
    unstow.add_argument('-B', '--unstow-bin',
                        action='store_true',
                        help='')
    args = parser.parse_args()

    CheckEnv.args_required_else_help()

    CheckEnv.root_check(require_root=True)

    run = Symlink()
    run.run(args)
