# -*- coding: utf-8 -*-
# 1.4.0
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
from collections import namedtuple
from pathlib import Path

from loguru import logger


class Count:
    def __init__(self, args: argparse = None):
        Ranges = namedtuple('Ranges', ['dest', 'lower', 'upper'])

        self.__size_ranges = (
            # 0B - 10MiB
            Ranges('10M', 0, 10 * 1024 * 1024),
            # 10MiB - 100MiB
            Ranges('100M', 10 * 1024 * 1024, 100 * 1024 * 1024),
            # 100MiB - 150MiB
            Ranges('150M', 100 * 1024 * 1024, 150 * 1024 * 1024),
            # 150MiB - 200MiB
            Ranges('200M', 150 * 1024 * 1024, 200 * 1024 * 1024),
            # 200MiB - 500MiB
            Ranges('500M', 200 * 1024 * 1024, 500 * 1024 * 1024),
            # 500MiB - 1GiB
            Ranges('1G', 500 * 1024 * 1024, 1 * 1024 * 1024 * 1024),
            # 1GiB - 10GiB
            Ranges('10G', 1 * 1024 * 1024 * 1024, 10 * 1024 * 1024 * 1024),
            # 10GiB - 100GiB
            Ranges('100G', 10 * 1024 * 1024 * 1024, 100 * 1024 * 1024 * 1024),
        )

        self.__file_list_done = []
        self.__file_list = []
        for f in Path(Path.cwd()).iterdir():
            if f.is_file():
                self.__file_list.append(f)

        self.run(args=args)

    def main_move(self):
        for ranges in self.__size_ranges:
            if len(self.__file_list) == 0:
                break

            dest = Path(ranges.dest).resolve()
            for idx, item in enumerate(self.__file_list):
                try:
                    file = Path(item)
                    size = Path.stat(file).st_size
                except FileNotFoundError:
                    continue

                if ranges.lower <= size <= ranges.upper:
                    if not Path.exists(dest):
                        dest.mkdir(parents=True, exist_ok=True)
                    Path.rename(file, Path() / dest / file.name)
                    self.__file_list_done.append(item)

            for idx, item in enumerate(self.__file_list_done):
                self.__file_list.remove(item)
            self.__file_list_done = []

    def run(self, args):
        self.main_move()


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

    Count(args=args)
