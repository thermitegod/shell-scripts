#!/usr/bin/env python3

# Copyright (C) 2018-2022 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# SCRIPT INFO
# 1.3.0
# 2021-04-29


import argparse
import shutil
import sys
from collections import namedtuple

from loguru import logger

from utils.recursion import RecursiveFindFiles


class RemoveJunk:
    def __init__(self, args: argparse = None):

        Junk = namedtuple('Junk', ['name', 'is_dir'])

        self.__junk = (
            Junk('desktop.ini', False),
            Junk('Thumbs.db', False),
            Junk('.DS_Store', False),
            Junk('__MACOSX', True),

            # Junk('', True),
            # Junk('', True),
            # Junk('', True),
        )

        self.__file_list_done = []
        self.__file_list_only = []
        self.__file_list = []

        self.parse_args(args=args)

    def main(self, list_only: bool = False):
        self.__file_list = RecursiveFindFiles(inc_dirs=True).get_files(pathlib=True)

        for junk in self.__junk:
            if len(self.__file_list) == 0:
                break

            for idx, item in enumerate(self.__file_list):
                if item.name == junk.name:
                    if list_only:
                        self.__file_list_done.append(item)
                        self.__file_list_only.append(item)
                    else:
                        self.__file_list_done.append(item)
                        if junk.is_dir:
                            shutil.rmtree(item)
                        else:
                            item.unlink()

            for idx, item in enumerate(self.__file_list_done):
                self.__file_list.remove(item)
            self.__file_list_done = []

            if self.__file_list_only:
                print(f'Found {junk.name}')
                print(f'==========================')
                for f in self.__file_list_only:
                    print(f)
                print('\n')
                self.__file_list_only = []

    def parse_args(self, args):
        if args.list:
            self.main(list_only=True)
        else:
            self.main()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='List files that match patern')
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

    RemoveJunk(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
