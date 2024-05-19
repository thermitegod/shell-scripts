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
# 4.7.1
# 2021-07-24


import argparse
import sys

from loguru import logger

from utils.execute import Execute
from utils.root_check import RootCheck


class Install:
    def __init__(self, args: argparse = None):
        self.__verbose = 'quiet'
        self.__kernel_ebuild = 'sys-kernel/gentoo-sources'

        self.parse_args(args=args)

        Execute(f'emerge --ignore-default-opts --oneshot --{self.__verbose} {self.__kernel_ebuild}')

        from utils.kernel import Kernel

        if not Kernel.write_running_config():
            logger.error('Unable to write running kernel .config')

    def parse_args(self, args):
        if args.verbose:
            self.__verbose = 'verbose'

        if args.git:
            self.__kernel_ebuild = 'sys-kernel/git-sources'
        elif args.vanilla:
            self.__kernel_ebuild = 'sys-kernel/vanilla-sources'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose install')
    group1 = parser.add_argument_group('kernels', 'default kernel to install is sys-kernel/gentoo-sources')
    group1.add_argument('-G', '--git',
                        action='store_true',
                        help='install sys-kernel/git-sources')
    group1.add_argument('-V', '--vanilla',
                        action='store_true',
                        help='install sys-kernel/vanilla-sources')
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

    RootCheck(require_root=True)

    Install(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
