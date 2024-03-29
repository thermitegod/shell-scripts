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
# 1.10.0
# 2021-04-29


import argparse
import sys

from loguru import logger

from utils.check_env import CheckEnv
from utils.recursion import RecursiveFindFiles


class Count:
    def __init__(self, args: argparse = None):
        self.__type_archive = ('.zip', '.7z', '.rar', '.cbr', '.cbz', '.cb7', '.tar',
                               '.bz2', '.gz', '.lz4', '.lzo', '.xz', '.zst')
        self.__type_image = ('.png', '.jpg', '.jpeg', '.jxl', '.jpe', '.gif', '.bmp', '.ico', )
        self.__type_video = ('.webm', '.mp4', '.mkv', '.avi', '.mov', '.wmv')

        script = CheckEnv.get_script_name()
        if script == 'count-image':
            self.__mode = self.__type_image
        elif script == 'count-archive':
            self.__mode = self.__type_archive
        elif script == 'count-video':
            self.__mode = self.__type_video
        else:
            print(f'Unknown mode: {script}')
            raise SystemExit(1)

        self.__list = False

        self.__counter = 0
        self.__counter_total = 0

        self.__file_list_done = []
        self.__file_list = []

        self.parse_args(args=args)

        if self.__list:
            self.main_list()
        else:
            self.main_count()

    def main_count(self):
        self.__file_list = RecursiveFindFiles().get_files(pathlib=True)

        for ext in self.__mode:
            if len(self.__file_list) == 0:
                break

            for idx, item in enumerate(self.__file_list):
                if item.suffix == ext:
                    self.__counter += 1
                    self.__file_list_done.append(item)

            for idx, item in enumerate(self.__file_list_done):
                self.__file_list.remove(item)
            self.__file_list_done = []

            if self.__counter != 0:
                print(f'{ext[1:].upper()}\t: {self.__counter}')
                self.__counter_total += self.__counter
                self.__counter = 0

        if self.__counter_total != 0:
            print(f'Total\t: {self.__counter_total}')

    def main_list(self):
        self.__file_list = RecursiveFindFiles().get_files()

        for ext in self.__mode:
            print(f'Listing all of: {ext[1:].upper()}')
            for f in self.__file_list:
                if f.endswith(ext):
                    print(f)

    def parse_args(self, args):
        if args.list:
            self.__list = True


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

    Count(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
