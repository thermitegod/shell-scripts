#!/usr/bin/env python3
# 1.3.1
# 2020-10-08

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
import os
from pathlib import Path

from utils import confirm
from utils import utils


class Backup:
    def __init__(self):
        self.__tape = '/dev/st0'
        self.__target = None

    def t_rewind(self):
        utils.run_cmd(f'mt -f \'{self.__tape}\' rewind')

    def t_status(self):
        utils.run_cmd(f'mt -f \'{self.__tape}\' status')

    def t_reten(self):
        utils.run_cmd(f'mt -f \'{self.__tape}\' retension')

    def t_eject(self):
        utils.run_cmd(f'mt -f \'{self.__tape}\' eject')

    def t_erase(self):
        utils.run_cmd(f'mt -f \'{self.__tape}\' erase')

    def t_list(self):
        utils.run_cmd(f'tar -tf \'{self.__tape}\'')

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
        utils.run_cmd(f'mt -f \'{self.__tape}\' eod')
        utils.run_cmd(f'tar -cvf \'{self.__tape}\' \'{self.__target}\'')

    def t_backup_overwrite(self):
        self.t_cdloc()
        self.t_rewind()
        utils.run_cmd(f'tar -cvf \'{self.__tape}\' \'{self.__target}\'')

    def t_restore(self):
        self.t_rewind()
        self.__target.mkdir(parents=True, exist_ok=True)
        utils.run_cmd(f'tar -xvf \'{self.__tape}\' -C \'{self.__target}\'')

    def t_verify(self):
        self.t_rewind()
        utils.run_cmd(f'tar -tvf \'{self.__tape}\'')

    def run(self, args):
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
    parser.add_argument('-b', '--backup',
                        metavar='FILE/DIR',
                        type=list,
                        nargs=1,
                        help='backup <input> at end of last backup on <tape>')
    parser.add_argument('-B', '--backup-overwrite',
                        metavar='FILE/DIR',
                        type=list,
                        nargs=1,
                        help='backup <input> at start, overwriting existing, on <tape>')
    parser.add_argument('-e', '--eject',
                        store='store_true',
                        help='eject tape')
    parser.add_argument('-g', '--restore',
                        metavar='DIR',
                        type=list,
                        nargs=1,
                        help='restore from begining of <tape> to <input>')
    parser.add_argument('-l', '--list',
                        store='store_true',
                        help='list contents of <tape>')
    parser.add_argument('-R', '--retension',
                        store='store_true',
                        help='tape retensioning <only for tape read errors>')
    parser.add_argument('-r', '--rewind',
                        store='store_true',
                        help='rewind tape')
    parser.add_argument('-s', '--status',
                        store='store_true',
                        help='drive status')
    parser.add_argument('-v', '--verify',
                        store='store_true',
                        help='verify files on current tape')
    parser.add_argument('-z', '--erase',
                        store='store_true',
                        help='erase/rewind tape')
    parser.add_argument('-Z', '--erase-eject',
                        store='store_true',
                        help='erase/rewind/eject tape')
    args = parser.parse_args()

    utils.root_check(require_root=True)

    utils.args_required_else_help()

    run = Backup()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
