# -*- coding: utf-8 -*-
# 1.5.0
# 2021-01-13

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
from collections import namedtuple
from pathlib import Path

from loguru import logger

from python.utils.recursion import RecursiveFindFiles


class Count:
    def __init__(self):
        Ranges = namedtuple('Ranges', ['group', 'lower', 'upper'])

        self.__size_ranges = (
            # 0B - 10MiB
            Ranges('0B-10M   ', 0, 10 * 1024 * 1024),
            # 10MiB - 100MiB
            Ranges('10M-100M ', 10 * 1024 * 1024, 100 * 1024 * 1024),
            # 100MiB - 150MiB
            Ranges('100M-150M', 100 * 1024 * 1024, 150 * 1024 * 1024),
            # 150MiB - 200MiB
            Ranges('150M-200M', 150 * 1024 * 1024, 200 * 1024 * 1024),
            # 200MiB - 500MiB
            Ranges('200M-500M', 200 * 1024 * 1024, 500 * 1024 * 1024),
            # 500MiB - 1GiB
            Ranges('500M-1G  ', 500 * 1024 * 1024, 1 * 1024 * 1024 * 1024),
            # 1GiB - 10GiB
            Ranges('1G-10G   ', 1 * 1024 * 1024 * 1024, 10 * 1024 * 1024 * 1024),
            # 10GiB - 100GiB
            Ranges('10G-100G ', 10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024),
        )

        self.__counter = 0
        self.__counter_total = 0

        self.__file_list_done = []
        self.__file_list = []

    def main_count(self):
        self.__file_list = RecursiveFindFiles().get_files(pathlib=True)

        for ranges in self.__size_ranges:
            if len(self.__file_list) == 0:
                break

            for idx, item in enumerate(self.__file_list):
                size = Path.stat(Path(item)).st_size

                if ranges.lower <= size <= ranges.upper:
                    self.__counter += 1
                    self.__file_list_done.append(item)

            for idx, item in enumerate(self.__file_list_done):
                self.__file_list.remove(item)
            self.__file_list_done = []

            if self.__counter != 0:
                print(f'{ranges.group} \t: {self.__counter}')
                self.__counter_total += self.__counter
                self.__counter = 0

        if self.__counter_total != 0:
            print(f'\nTotal\t\t: {self.__counter_total}')

    def run(self):
        self.main_count()


def main():
    parser = argparse.ArgumentParser()
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

    run = Count()
    run.run()
