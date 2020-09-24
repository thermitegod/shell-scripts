#!/usr/bin/env python3
# 1.0.0
# 2020-09-24

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
import sys
from pathlib import Path

from loguru import logger

from utils import hash
from utils import natural_sort


class Count:
    def __init__(self):
        self.__file_counter = 0
        self.__counter_total = 0

        self.__padding = None

        self.__file_list = []

    def count_files(self):
        for f in Path(Path.cwd()).iterdir():
            if f.is_file():
                self.__file_list.append(str(Path(f).name))
                self.__file_counter += 1

        natural_sort.alphanumeric_sort(self.__file_list)

    def set_padding(self):
        if self.__file_counter >= 1000:
            self.__padding = f'04'
        else:
            self.__padding = f'03'

    def reset_vars(self):
        self.__file_counter = 0
        self.__counter_total = 0
        self.__padding = None
        self.__file_list = []

    def rename_files(self):
        count = 1
        for f in self.__file_list:
            ext = f.rpartition('.')[-1]
            file_original = Path(f).resolve()
            file_new = Path() / Path.cwd() / f'{count:{self.__padding}}.{ext}'

            if not Path.exists(Path(file_new)):
                Path.rename(file_original, file_new)
                logger.debug(f'Renamed \'{file_original}\' -> \'{file_new}\'')
            else:
                if hash.file_hash_compare(file_original, file_new):
                    logger.debug(f'Same File not renaming: \'{file_new}\'')
                else:
                    logger.critical(f'===SHOULD NEVER BE SEEN===')
                    logger.critical(f'Name collision with a diffrent file: \'{file_new}\'')

            count += 1

    def recursive_find(self):
        for f in Path(Path.cwd()).iterdir():
            if f.is_dir():
                os.chdir(f)
                self.main_rename()
                self.recursive_find()

    def main_rename(self):
        self.count_files()

        if self.__file_counter != 0:
            self.set_padding()
            self.rename_files()
        else:
            logger.debug(f'No file to rename in \'{Path.cwd()}\'')

        self.reset_vars()

    def run(self, args):
        if args.batch:
            self.recursive_find()
        else:
            self.main_rename()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--batch',
                        action='store_true',
                        help='Rename all files in all subdirectories numerically')
    debug = parser.add_argument_group('DEBUG')
    debug.add_argument('-L', '--loglevel',
                       default='DEBUG',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    run = Count()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
