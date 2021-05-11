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
import shutil
import sys
from pathlib import Path

from loguru import logger

from python.utils.execute import Execute


class Trash:
    def __init__(self, args: argparse = None):
        self.__trashdir = Path('/tmp/.Trash-1000')

        self.parse_args(args=args)

    def remove(self):
        if Path.is_dir(self.__trashdir):
            shutil.rmtree(self.__trashdir)

    def size(self):
        if Path.is_dir(self.__trashdir):
            Execute(f'du -h {self.__trashdir} | tail -n1 | awk \'{{print $1}}\'',
                    sh_wrap=True)
        else:
            print(f'There is no trash dir: {self.__trashdir}')

    def parse_args(self, args):
        if args.remove:
            self.remove()
        elif args.size:
            self.size()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size',
                        action='store_true',
                        help='Print size of trash dir')
    parser.add_argument('-r', '--remove',
                        action='store_true',
                        help='Remove trash dir')
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

    Trash(args=args)
