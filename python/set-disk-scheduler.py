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


class Scheduler:
    def __init__(self):
        self.__pool_storage = ['sda', 'sdb', 'sdc', 'sdd', 'sde', 'sdf', 'sdg', 'sdh', 'sdk', 'sdi', 'sdm', 'sdn']
        self.__pool_torrents = ['sdm', 'sdn']
        self.__pool_ssd = ['sdl', 'sdj']
        self.__pool_root = ['nvme0n1', 'nvme1n1']
        self.__disks = self.__pool_storage + self.__pool_torrents + self.__pool_ssd + self.__pool_root

    @staticmethod
    def get_scheduler(disk):
        return Path.open(Path() / '/sys/block' / disk / 'queue/scheduler', 'r').read().partition(' ')[0]

    def run(self, args):
        if args.current:
            for disk in self.__disks:
                sched = self.get_scheduler(disk)
                print(f'Scheduler is {Colors.GRE}{sched}{Colors.NC} for {Colors.YEL}/dev/{disk}{Colors.NC}')
        if args.set:
            # not really needed with current setup but still porting from sh in case
            # it ever is needed for some reason

            utils.root_check(require_root=True)
            new_sched = args.set
            for disk in self.__disks:
                # will strip opening and closing []
                current_sched = self.get_scheduler(disk)[1:][:-1]
                if current_sched == new_sched:
                    print(f'Disk scheduler is already set to \'{current_sched}\'')
                else:
                    disk.write_text(new_sched)
                    print(f'Scheduler set to {Colors.GRE}[{new_sched}]{Colors.NC} for '
                          f'{Colors.YEL}/dev/{disk}{Colors.NC}\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--current',
                        action='store_true',
                        help='Get current GPU power state')
    parser.add_argument('-s', '--set',
                        metavar='STATE',
                        nargs=1,
                        choices=['mq-deadline', 'none'],
                        help='Set GPU power state')
    args = parser.parse_args()

    utils.args_required_else_help()

    run = Scheduler()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
