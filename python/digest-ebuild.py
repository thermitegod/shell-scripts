#!/usr/bin/env python3
# 1.0.0
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
import os
import sys
from pathlib import Path

from loguru import logger

from utils import utils


class Digest:
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

        utils.run_cmd(f'ebuild {ebuild_list[-1]} manifest')

    def recursive_find(self):
        for f in Path(Path.cwd()).iterdir():
            if f.is_dir():
                os.chdir(f)
                self.digest()
                self.recursive_find()

    def run(self, args):
        # general
        if args.all:
            self.recursive_find()
            raise SystemExit

        self.digest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all',
                        action='store_true',
                        help='run for the entire repo')
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

    run = Digest()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
