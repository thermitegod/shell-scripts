#!/usr/bin/env python3

# Copyright (C) 2018-2022 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# SCRIPT INFO
# 2.1.0
# 2022-12-08


import argparse
import os
import sys
from pathlib import Path

from loguru import logger

from python.utils import repo

from python.utils.execute import Execute

class Symlink:
    def __init__(self, args: argparse = None):
        self.__repo_base_path = repo.repo_base_dir()

        self.__bin = self.__repo_base_path / 'bin'
        self.__local_bin = Path() / '/usr/local/bin'

        self.install_symlinks()

    def install_symlinks(self):
        os.chdir(self.__bin)
        for f in Path(Path.cwd()).iterdir():
            if Path.is_dir(f):
                continue

            real = Path(f)
            symlink = Path() / self.__local_bin / real.name
            if symlink.is_symlink() or real.name == '.keep':
                continue

            # print(f'{symlink} -> {real}')
            os.symlink(real, symlink)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user',
                        metavar='USER',
                        default='brandon',
                        help='user')
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

    if os.geteuid() != 0:
        logger.error('Requires root, exiting')
        raise SystemExit(1)

    Symlink(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
