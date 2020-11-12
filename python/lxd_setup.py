# -*- coding: utf-8 -*-
# 1.6.0
# 2020-11-11

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

from loguru import logger

from python.utils import lxd
from python.utils import utils


class Container:
    def __init__(self):
        self.__base_container = 'dev-gentoo-clang-minimal'
        self.__base_rutorrent = 'base-gentoo-rutorrent'
        self.__base_transmission = 'base-gentoo-transmission'

    def stop_base(self):
        logger.info(f'Stopping {self.__base_container}')
        utils.run_cmd(f'lxc stop {self.__base_container}', to_stdout=True)

    def update_generic(self, container, setup_script):
        if lxd.get_state(container=container):
            logger.info(f'Stopping {container}')
            utils.run_cmd(f'lxc stop {container}', to_stdout=True)

        logger.info(f'Deleting {container}')
        utils.run_cmd(f'lxc delete {container}', to_stdout=True)

        logger.info(f'copying {self.__base_container} to {container}')
        utils.run_cmd(f'lxc copy {self.__base_container} {container}', to_stdout=True)

        logger.info(f'Starting {container}')
        utils.run_cmd(f'lxc start {container}', to_stdout=True)

        logger.info(f'Running setup script for {container}')
        utils.run_cmd(f'lxc exec {container} {setup_script}', to_stdout=True)

        logger.info(f'Stopping {container}')
        utils.run_cmd(f'lxc stop {container}', to_stdout=True)

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

    run = Container()
    run.run(args)
