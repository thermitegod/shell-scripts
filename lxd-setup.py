#!/usr/bin/env python3
# 1.0.0
# 2020-05-06

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
import time

from utils import utils


class Container:
    def __init__(self):
        self.__base_container = 'dev-gentoo-clang-minimal'
        self.__base_rutorrent = 'base-gentoo-rutorrent'
        self.__base_transmission = 'base-gentoo-transmission'

    def stop_base(self):
        print(f'Stoping {self.__base_container}')
        utils.run_cmd(f'lxc stop {self.__base_container}')

    def update_generic(self, container, setup_script):
        print(f'Stopping {container}')
        utils.run_cmd(f'lxc stop {container}')

        print(f'Deleting {container}')
        utils.run_cmd(f'lxc delete {container}')

        print(f'copying {self.__base_container} to {container}')
        utils.run_cmd(f'lxc copy {self.__base_container} {container}')

        print(f'Starting {self.__base_rutorrent}')
        utils.run_cmd(f'lxc start {container}')

        # make sure everyting has started
        time.sleep(2)

        print(f'Running setup script for {container}')
        utils.run_cmd(f'lxc exec base-gentoo-rutorrent {setup_script}')

        print(f'Stopping {container}')
        utils.run_cmd(f'lxc stop {container}')

    def update_rutorrent(self):
        self.update_generic(container=self.__base_rutorrent,
                            setup_script='/root/setup-rutorrent.sh')

    def update_transmission(self):
        self.update_generic(container=self.__base_transmission,
                            setup_script='/root/setup-transmission.sh')

    def run(self, args):
        self.stop_base()

        if args.rutorrent:
            self.update_rutorrent()

        if args.transmission:
            self.update_transmission()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rutorrent',
                        default=True,
                        action='store_false',
                        help='Do not update rutorrent base container')
    parser.add_argument('-t', '--transmission',
                        default=True,
                        action='store_false',
                        help='Do not update transmission base container')
    args = parser.parse_args()

    run = Container()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
