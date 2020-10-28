#!/usr/bin/env python3
# 1.2.0
# 2020-10-28

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
from pathlib import Path

from utils import utils
from utils.colors import Colors


class Powerstate:
    def __init__(self):
        self.__card = Path() / '/sys/class/drm/card0/device/power_dpm_force_performance_level'
        self.__current_state = Path.open(self.__card, 'r').read().rstrip()

    def run(self, args):
        if args.current:
            print(f'Current GPU power state is: {Colors.GRE}{self.__current_state}{Colors.NC}')
        if args.set:
            new_state = args.set
            if self.__current_state == new_state:
                print(f'GPU state is already \'{self.__current_state}\'')
                raise SystemExit

            utils.root_check(require_root=True)

            print(f'Current GPU power state is \'{self.__current_state}\', switching state to \'{new_state}\'')
            self.__card.write_text(new_state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--current',
                        action='store_true',
                        help='Get current GPU power state')
    parser.add_argument('-s', '--set',
                        metavar='STATE',
                        choices=['auto', 'low', 'high'],
                        help='Set GPU power state')
    args = parser.parse_args()

    utils.args_required_else_help()

    run = Powerstate()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
