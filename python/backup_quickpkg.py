# -*- coding: utf-8 -*-
# 1.7.0
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
import atexit
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

from loguru import logger

from python.utils.check_env import CheckEnv
from python.utils.execute import Execute
from python.utils.root_check import RootCheck


class Backup:
    def __init__(self, args: argparse = None):
        atexit.register(self.remove_tmpdir)
        self.__tmpdir = tempfile.mkdtemp()

        self.__verbose = ''

        self.__backup_dir = Path() / '/mnt/data/backup/gentoo'

        self.__mode = None

        self.__user = None

        self.__date = time.strftime('%Y-%m-%d', time.localtime())

        self.parse_args(args=args)
        self.backup()

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

    def move_finished(self, dest: Path):
        dest.mkdir(parents=True, exist_ok=True)
        os.chdir(self.__tmpdir)
        for f in Path.cwd().iterdir():
            if f.is_file():
                Execute(f'mv -- {f} {dest}')

    def backup(self):
        print(self.__mode)
        if self.__mode == '1':
            # packages
            target_dest = Path() / self.__backup_dir / 'packages'
            target_dest.mkdir(parents=True, exist_ok=True)

            pkgdir = Path() / self.__tmpdir / f'packages-{self.__date}'
            pkgdir.mkdir(parents=True, exist_ok=True)

            Execute(f'PKGDIR={pkgdir} quickpkg --include-config=y "*/*"', sh_wrap=True)

            Execute(f'mv -i -- {pkgdir} {target_dest}')

        elif self.__mode == '2':
            # repos
            target_dest = Path() / self.__backup_dir / 'repos' / self.__date

            os.chdir('/var/db')
            Execute(f'mkzst {self.__verbose} -o {self.__tmpdir} repos')

            self.move_finished(dest=target_dest)

        elif self.__mode == '3':
            # portage_etc
            target_dest = Path() / self.__backup_dir / 'portage' / self.__date

            os.chdir('/etc')
            Execute(f'mkzst {self.__verbose} -o {self.__tmpdir} portage')

            self.move_finished(dest=target_dest)

        elif self.__mode == '4':
            # portage_world
            target_dest = Path() / self.__backup_dir / 'world' / self.__date

            os.chdir('/var/lib/portage')
            Execute(f'mkzst {self.__verbose} -o {self.__tmpdir} world')

            self.move_finished(dest=target_dest)

        elif self.__mode == '5':
            # all
            Execute(f'{CheckEnv.get_script_name()} -m 1')
            Execute(f'{CheckEnv.get_script_name()} -m 2')
            Execute(f'{CheckEnv.get_script_name()} -m 3')
            Execute(f'{CheckEnv.get_script_name()} -m 4')

    def parse_args(self, args):
        if args.verbose:
            self.__verbose = '-v'
        if args.user:
            self.__user = args.user
        if args.mode:
            self.__mode = args.mode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose tar')
    parser.add_argument('-u', '--user',
                        metavar='USER',
                        default='brandon',
                        help='user')
    parser.add_argument('-m', '--mode',
                        metavar='MODE',
                        default='3',
                        choices=['1', '2', '3', '4', '5'],
                        help='Selects backup to run',)
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

    Backup(args=args)
