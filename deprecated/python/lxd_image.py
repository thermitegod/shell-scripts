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
import datetime
import sys
from pathlib import Path

from loguru import logger

from utils.execute import Execute
from utils.lxd import Lxd


class Container:
    def __init__(self, args: argparse = None):
        super().__init__()

        time = datetime.datetime.now()
        year = str(time.year)
        month = str(time.month)
        day = str(time.day)
        current_date = f'{year}-{month}-{day}'

        self.__backup_dir = Path() / '/mnt/data/backup/lxd' / current_date

        self.parse_args(args=args)

    def export_container(self, container):
        if not Path.is_dir(self.__backup_dir):
            if Path.exists(self.__backup_dir):
                print(f'Backup dir \'{self.__backup_dir}\' exists but is not a directory')
                raise SystemExit(1)
            self.__backup_dir.mkdir(parents=True, exist_ok=True)

        if Lxd.get_state(container=container):
            logger.info(f'Stoping {container}')
            Execute(f'lxc stop {container}', to_stdout=True)

        Execute(f'lxc export {container} {self.__backup_dir}/{container}.tar.gz')

    @staticmethod
    def install_container(container: Path):
        if not Path.is_file(container):
            logger.error(f'Cannont locate \'{container}\', enter file path')
            raise SystemExit

        logger.info(f'Importing {container}')
        Execute(f'lxc import {container}', to_stdout=True)

    def parse_args(self, args):
        if args.export:
            self.export_container(container=args.export)

        if args.install:
            self.install_container(container=Path(args.install))


def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required exclusive arguments').add_mutually_exclusive_group(required=True)
    required.add_argument('-e', '--export',
                          metavar='CONTAINER',
                          help='Export lxd container to file')
    required.add_argument('-i', '--install',
                          metavar='FILE',
                          help='Import lxd container from file')
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
