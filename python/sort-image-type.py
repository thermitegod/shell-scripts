#!/usr/bin/env python3
# 1.1.1
# 2020-10-04

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
from pathlib import Path

from loguru import logger

from utils import utils


class Sort:
    def __init__(self):
        self.__type = ('.jpg', '.png', '.gif', '.webm', '.mp4', '.zip', '.mkv', '.rar')

        self.__mode = None

    def main_sort(self):
        for ext in self.__type:
            dest = ext[1:]
            cwd = Path.cwd()
            if self.__mode == 'dir_check':
                utils.run_cmd(f'find . -maxdepth 1 -type f -iname "*{ext}" -exec mkdir -p "{cwd}/{dest}" \\; -quit')
            elif self.__mode == 'loop_main':
                utils.run_cmd(f'find . -maxdepth 1 -type f -iname "*{ext}" -exec mv -i -- "{{}}" "{cwd}/{dest}" \\;')

    def run(self, args):
        self.__mode = 'dir_check'
        self.main_sort()
        self.__mode = 'loop_main'
        self.main_sort()


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

    run = Sort()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
