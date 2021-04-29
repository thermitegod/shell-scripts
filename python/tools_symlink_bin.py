#!/usr/bin/env python3
# 1.9.0
# 2021-04-29

# Copyright (C) 2020,2021 Brandon Zorn <brandonzorn@cock.li>
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

from python.utils.execute import Execute
from python.utils.root_check import RootCheck


class Symlink:
    def __init__(self, args: argparse = None):
        # since root is req to do this Path.home() will return
        # /root so create wanted home path
        self.__home = None
        self.__local_bin = Path() / '/usr/local/bin'

        self.__ignore = '--ignore=".git" ' \
                        '--ignore=".idea" ' \
                        '--ignore=".gitignore" ' \
                        '--ignore="deprecated" ' \
                        '--ignore="python" ' \
                        '--ignore="shell" ' \
                        '--ignore="tools" ' \
                        '--ignore="utils" '

        self.run(args=args)

    def run(self, args):
        if args.user:
            self.__home = Path() / '/home' / args.user
        if args.stow_bin:
            os.chdir(self.__home)
            Execute(f'stow {self.__ignore} -v --target={self.__local_bin} .bin')
        if args.unstow_bin:
            os.chdir(self.__home)
            Execute(f'stow {self.__ignore} -D -v --target={self.__local_bin} .bin')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user',
                        metavar='USER',
                        default='brandon',
                        help='user')
    stow = parser.add_argument_group('stow').add_mutually_exclusive_group(required=True)
    stow.add_argument('-b', '--stow-bin',
                      action='store_true',
                      help='')
    unstow = parser.add_argument_group('unstow')
    unstow.add_argument('-B', '--unstow-bin',
                        action='store_true',
                        help='')
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

    RootCheck(require_root=True)

    Symlink(args=args)
