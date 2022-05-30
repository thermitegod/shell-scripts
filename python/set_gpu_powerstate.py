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
# 1.7.0
# 2021-04-29


import argparse
import sys
from pathlib import Path

from loguru import logger

from utils.colors import Colors
from utils.root_check import RootCheck


class Powerstate:
    def __init__(self, args: argparse = None):
        self.__card = Path() / '/sys/class/drm/card0/device/power_dpm_force_performance_level'
        self.__current_state = Path.open(self.__card, 'r').read().rstrip()

        self.parse_args(args=args)

    def parse_args(self, args):
        if args.current:
            print(f'Current GPU power state is: {Colors.GRE}{self.__current_state}{Colors.NC}')
        if args.set:
            new_state = args.set
            if self.__current_state == new_state:
                print(f'GPU state is already \'{self.__current_state}\'')
                raise SystemExit

            RootCheck(require_root=True)

            print(f'Current GPU power state is \'{self.__current_state}\', switching state to \'{new_state}\'')
            self.__card.write_text(new_state)


def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required exclusive arguments').add_mutually_exclusive_group(required=True)
    required.add_argument('-c', '--current',
                          action='store_true',
                          help='Get current GPU power state')
    required.add_argument('-s', '--set',
                          metavar='STATE',
                          choices=['auto', 'low', 'high'],
                          help='Set GPU power state')
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

    Powerstate(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
