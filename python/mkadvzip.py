# -*- coding: utf-8 -*-
# 1.5.0
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


class Optimize:
    def __init__(self, args: argparse = None):
        self.__verbose = False

        self.__size_start = 0
        self.__size_end = 0

        self.__cpu = os.cpu_count()

        self.parse_args(args=args)

        self.main()

    def get_size(self, start: bool):
        size = sum(f.stat().st_size for f in Path.cwd().glob('**/*') if f.is_file())
        if start:
            self.__size_start = size
        else:
            self.__size_end = size

    def main(self):
        if self.__verbose:
            self.get_size(start=True)

        Execute(f'find . -type f -iname \'*.zip\' -print0 | '
                f'nice -19 xargs --max-args=1 --max-procs={self.__cpu} --null '
                f'advzip -z -4',
                sh_wrap=True)

        if self.__verbose:
            self.get_size(start=False)
            print(f'Before     : {self.__size_start}\n'
                  f'After      : {self.__size_end}\n'
                  f'% of orig  : {self.__size_end / self.__size_start}')

    def parse_args(self, args):
        if args.verbose:
            self.__verbose = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Print change in dir size')
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

    Optimize(args=args)
