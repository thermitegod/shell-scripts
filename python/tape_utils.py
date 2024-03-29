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
# 1.9.0
# 2021-04-29


import argparse
import os
import sys
from pathlib import Path

from loguru import logger

from utils import confirm
from utils.execute import Execute
from utils.root_check import RootCheck


class Backup:
    def __init__(self, args: argparse = None):
        self.__tape = '/dev/st0'
        self.__target = None

        self.parse_args(args=args)

    def t_rewind(self):
        Execute(f'mt -f \'{self.__tape}\' rewind')

    def t_status(self):
        Execute(f'mt -f \'{self.__tape}\' status')

    def t_reten(self):
        Execute(f'mt -f \'{self.__tape}\' retension')

    def t_eject(self):
        Execute(f'mt -f \'{self.__tape}\' eject')

    def t_erase(self):
        Execute(f'mt -f \'{self.__tape}\' erase')

    def t_list(self):
        Execute(f'tar -tf \'{self.__tape}\'')

    def t_cdloc(self):
        # dont tar unneeded paths
        if Path.is_dir(self.__target):
            os.chdir(self.__target.parent)
        elif Path.is_file(self.__target):
            os.chdir(self.__target.parent)
        else:
            print('Not a file or directory')
            raise SystemExit(1)

    def t_confirm_erase(self):
        if confirm.confirm_run('Confirm erase current tape [y/n]? '):
            self.t_erase()
        else:
            print('Did not confirm, Exiting')
            raise SystemExit(1)

    def t_backup(self):
        self.t_cdloc()

        # move to end last tar on tape
        Execute(f'mt -f \'{self.__tape}\' eod')
        Execute(f'tar -cvf \'{self.__tape}\' \'{self.__target}\'')

    def t_backup_overwrite(self):
        self.t_cdloc()
        self.t_rewind()
        Execute(f'tar -cvf \'{self.__tape}\' \'{self.__target}\'')

    def t_restore(self):
        self.t_rewind()
        self.__target.mkdir(parents=True, exist_ok=True)
        Execute(f'tar -xvf \'{self.__tape}\' -C \'{self.__target}\'')

    def t_verify(self):
        self.t_rewind()
        Execute(f'tar -tvf \'{self.__tape}\'')

    def parse_args(self, args):
        # general
        if args.backup:
            self.__target = Path() / args.backup
            self.t_backup()
        if args.backup_overwrite:
            self.__target = Path() / args.backup_overwrite
            self.t_backup_overwrite()
        if args.eject:
            self.t_eject()
        if args.restore:
            self.__target = Path() / args.restore
            self.t_restore()
        if args.list:
            self.t_list()
        if args.retension:
            self.t_reten()
        if args.rewind:
            self.t_rewind()
        if args.status:
            self.t_status()
        if args.verify:
            self.t_verify()
        if args.erase:
            self.t_confirm_erase()
            self.t_rewind()
        if args.erase_eject:
            self.t_confirm_erase()
            self.t_rewind()
            self.t_eject()


def main():
    parser = argparse.ArgumentParser()
    exclusive = parser.add_argument_group('required exclusive arguments').add_mutually_exclusive_group(required=True)
    exclusive.add_argument('-b', '--backup',
                           metavar='FILE/DIR',
                           type=list,
                           nargs=1,
                           help='backup <input> at end of last backup on <tape>')
    exclusive.add_argument('-B', '--backup-overwrite',
                           metavar='FILE/DIR',
                           type=list,
                           nargs=1,
                           help='backup <input> at start, overwriting existing, on <tape>')
    exclusive.add_argument('-e', '--eject',
                           action='store_true',
                           help='eject tape')
    exclusive.add_argument('-g', '--restore',
                           metavar='DIR',
                           type=list,
                           nargs=1,
                           help='restore from begining of <tape> to <input>')
    exclusive.add_argument('-l', '--list',
                           action='store_true',
                           help='list contents of <tape>')
    exclusive.add_argument('-R', '--retension',
                           action='store_true',
                           help='tape retensioning <only for tape read errors>')
    exclusive.add_argument('-r', '--rewind',
                           action='store_true',
                           help='rewind tape')
    exclusive.add_argument('-s', '--status',
                           action='store_true',
                           help='drive status')
    exclusive.add_argument('-v', '--verify',
                           action='store_true',
                           help='verify files on current tape')
    exclusive.add_argument('-z', '--erase',
                           action='store_true',
                           help='erase/rewind tape')
    exclusive.add_argument('-Z', '--erase-eject',
                           action='store_true',
                           help='erase/rewind/eject tape')
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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
