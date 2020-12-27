# -*- coding: utf-8 -*-
# 2.0.1
# 2020-12-26

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
import sys
from collections import namedtuple
from pathlib import Path

from loguru import logger


class SortImg:
    def __init__(self):
        super().__init__()

        Sort = namedtuple('Sort', ['ext', 'save'])

        self.__list_sort = (
            Sort('.jpg', 'JPG'),
            Sort('.jpeg', 'JEPG'),
            Sort('.png', 'PNG'),
            Sort('.gif', 'GIF'),

            Sort('.webm', 'WEBM'),
            Sort('.mp4', 'MP4'),
            Sort('.mkv', 'MKV'),

            Sort('.zip', 'ZIP'),
            Sort('.rar', 'RAR'),
        )

        self.__file_list_done = []
        self.__file_list = []
        for f in Path(Path.cwd()).iterdir():
            if f.is_file():
                self.__file_list.append(f)

        self.__total_after = None
        self.__total_before = len(self.__file_list)

    def sort(self):
        if self.__total_before == 0:
            logger.info(f'No files found')
            raise SystemExit

        for idx, item in enumerate(self.__list_sort):
            if len(self.__file_list) == 0:
                break

            ext = item.ext
            target = Path.cwd() / item.save

            for f in self.__file_list:
                # case insensitive pattern matching
                file = Path(f)
                if not file.suffix.lower() == ext:
                    continue

                if not Path.exists(target):
                    # all target dirs should exits before running
                    # otherwise you are going to have a bad time
                    target.mkdir(parents=True, exist_ok=True)

                if not Path.is_file(Path(target, file.name)):
                    # move maches to dest
                    Path.rename(file, Path(target, file.name))
                else:
                    logger.warning(f'Unable to sort: {f}')

                self.__file_list_done.append(f)

            for f in self.__file_list_done:
                self.__file_list.remove(f)
            self.__file_list_done = []

    def run(self, args):
        self.sort()

        self.__total_after = len(self.__file_list)

        print(f'\nTotal sorted')
        print(f'Before\t: {self.__total_before}')
        print(f'After\t: {self.__total_after}')
        print(f'Total\t: {self.__total_before - self.__total_after }')


def main():
    parser = argparse.ArgumentParser()
    debug = parser.add_argument_group('DEBUG')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    run = SortImg()
    run.run(args)
