# -*- coding: utf-8 -*-
# 1.6.0
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

from python.utils.execute import Execute
from python.utils.recursion import RecursiveExecute


class Digest:
    def __init__(self, args: argparse = None):
        self.parse_args(args=args)
        self.digest()

    @staticmethod
    def digest():
        ebuild_list = []
        for f in Path(Path.cwd()).iterdir():
            if str(f).endswith('.ebuild'):
                ebuild_list.append(f)

        if not ebuild_list:
            logger.debug(f'No ebuilds found')
            raise SystemExit

        ebuild_list.sort()

        Execute(f'ebuild {ebuild_list[-1]} manifest')

    def parse_args(self, args):
        # general
        if args.all:
            RecursiveExecute(function=self.digest)
            raise SystemExit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='run for the entire repo')
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

    Digest(args=args)
