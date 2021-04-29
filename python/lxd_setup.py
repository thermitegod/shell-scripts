# -*- coding: utf-8 -*-
# 1.10.0
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

from loguru import logger

from python.utils.execute import Execute
from python.utils.lxd import Lxd


class Container:
    def __init__(self, args: argparse = None):
        super().__init__()

        self.__base_container = Lxd.base_container
        self.__base_rutorrent = Lxd.base_rutorrent
        self.__base_transmission = Lxd.base_transmission

        self.run(args=args)

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

    def run(self, args):
        self.stop_base()

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
