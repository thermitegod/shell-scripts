# -*- coding: utf-8 -*-
# 1.10.0
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
import sys
from pathlib import Path

from loguru import logger

from python.utils import natural_sort
from python.utils.hash_compare import HashCompare
from python.utils.recursion import RecursiveExecute


class Count:
    def __init__(self, args: argparse = None):
        self.__file_counter = 0
        self.__counter_total = 0

        self.__padding = None

        self.__file_list = []

        self.__pretend = False

        self.run(args=args)

    def count_files(self):
        for f in Path(Path.cwd()).iterdir():
            if f.is_file():
                self.__file_list.append(str(Path(f).name))
                self.__file_counter += 1

        natural_sort.alphanumeric_sort(self.__file_list)

    def set_padding(self):
        if self.__file_counter <= 1000:
            self.__padding = f'03'
        else:
            self.__padding = f'0{len(str(self.__file_counter))}'

    def reset_vars(self):
        self.__file_counter = 0
        self.__counter_total = 0
        self.__padding = None
        self.__file_list = []

    def rename_files(self):
        for idx, item in enumerate(self.__file_list, start=1):
            ext = item.rpartition('.')[-1]
            file_original = Path(item).resolve()
            file_new = Path() / Path.cwd() / f'{idx:{self.__padding}}.{ext}'

            if not Path.exists(Path(file_new)):
                if self.__pretend:
                    logger.debug(f'[PRETEND] Renamed \'{file_original}\' -> \'{file_new}\'')
                    continue

                Path.rename(file_original, file_new)
                logger.debug(f'Renamed \'{file_original}\' -> \'{file_new}\'')
            else:
                if HashCompare(file_original, file_new).results():
                    logger.debug(f'Same File not renaming: \'{file_new}\'')
                else:
                    logger.critical(f'===SHOULD NEVER BE SEEN===')
                    logger.critical(f'Name collision with a diffrent file: \'{file_new}\'')

    def main_rename(self):
        self.count_files()

        if self.__file_counter != 0:
            self.set_padding()
            self.rename_files()
        else:
            logger.debug(f'No file to rename in \'{Path.cwd()}\'')

        self.reset_vars()

    def run(self, args):
        if args.pretend:
            self.__pretend = True
        if args.batch:
            RecursiveExecute(function=self.main_rename)
        else:
            self.main_rename()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--batch',
                        action='store_true',
                        help='Rename all files in all subdirectories numerically')
    parser.add_argument('-p', '--pretend',
                        action='store_true',
                        help='Rename all files in all subdirectories numerically')
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
