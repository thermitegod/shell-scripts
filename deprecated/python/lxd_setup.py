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
# 1.10.0
# 2021-04-29


import argparse
import sys

from loguru import logger

from utils.execute import Execute
from utils.lxd import Lxd


class Container:
    def __init__(self, args: argparse = None):
        super().__init__()

        self.__base_container = Lxd.base_container
        self.__base_rutorrent = Lxd.base_rutorrent
        self.__base_transmission = Lxd.base_transmission

        self.stop_base()
        self.parse_args(args=args)

    def stop_base(self):
        logger.info(f'Stopping {self.__base_container}')
        Execute(f'lxc stop {self.__base_container}', to_stdout=True)

    def update_generic(self, container, setup_script):
        if Lxd.get_state(container=container):
            logger.info(f'Stopping {container}')
            Execute(f'lxc stop {container}', to_stdout=True)

        logger.info(f'Deleting {container}')
        Execute(f'lxc delete {container}', to_stdout=True)

        logger.info(f'copying {self.__base_container} to {container}')
        Execute(f'lxc copy {self.__base_container} {container}', to_stdout=True)

        logger.info(f'Starting {container}')
        Execute(f'lxc start {container}', to_stdout=True)

        logger.info(f'Running setup script for {container}')
        Execute(f'lxc exec {container} {setup_script}', to_stdout=True)

        logger.info(f'Stopping {container}')
        Execute(f'lxc stop {container}', to_stdout=True)

    def parse_args(self, args):
        if args.rutorrent:
            self.update_generic(container=self.__base_rutorrent,
                                setup_script='/root/setup-rutorrent.sh')

        if args.transmission:
            self.update_generic(container=self.__base_transmission,
                                setup_script='/root/setup-transmission.sh')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rutorrent',
                        default=True,
                        action='store_false',
                        help='Do not update rutorrent base container')
    parser.add_argument('-t', '--transmission',
                        default=False,
                        action='store_true',
                        help='Do not update transmission base container')
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

    Container(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
