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
from pathlib import Path

from python.utils.colors import Colors
from python.utils.root_check import RootCheck


class Powerstate:
    def __init__(self, args: argparse = None):
        self.__card = Path() / '/sys/class/drm/card0/device/power_dpm_force_performance_level'
        self.__current_state = Path.open(self.__card, 'r').read().rstrip()

        self.run(args=args)

    def run(self, args):
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
    args = parser.parse_args()

    Powerstate(args=args)
