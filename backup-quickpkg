#!/usr/bin/env python3
# 1.0.0
# 2020-09-19

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
import atexit
import os
import shutil
import tempfile
import time
from pathlib import Path

from utils import utils


class Backup:
    def __init__(self):
        atexit.register(self.remove_tmpdir)
        self.__tmpdir = tempfile.mkdtemp()

        self.__verbose = ''

        self.__backup_dir = Path() / '/mnt/data/backup/gentoo'

        self.__mode = None

        self.__user = None

        self.__date = time.strftime('%Y-%m-%d', time.localtime())

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

    def move_finished(self, dest: Path):
        dest.mkdir(parents=True, exist_ok=True)
        os.chdir(self.__tmpdir)
        for f in Path.cwd().iterdir():
            if f.is_file():
                utils.run_cmd(f'mv -- {f} {dest}')

    def backup(self):
        print(self.__mode)
        if self.__mode == '1':
            # packages
            target_dest = Path() / self.__backup_dir / 'packages'
            target_dest.mkdir(parents=True, exist_ok=True)

            pkgdir = Path() / self.__tmpdir / f'packages-{self.__date}'
            pkgdir.mkdir(parents=True, exist_ok=True)

            utils.run_cmd(f'PKGDIR={pkgdir} quickpkg --include-config=y "*/*"', sh_wrap=True)

            utils.run_cmd(f'mv -i -- {pkgdir} {target_dest}')

        elif self.__mode == '2':
            # repos
            target_dest = Path() / self.__backup_dir / 'repos' / self.__date

            os.chdir('/var/db')
            utils.run_cmd(f'mkzst {self.__verbose} -o {self.__tmpdir} repos')

            self.move_finished(dest=target_dest)

        elif self.__mode == '3':
            # portage_etc
            target_dest = Path() / self.__backup_dir / 'portage' / self.__date

            os.chdir('/etc')
            utils.run_cmd(f'mkzst {self.__verbose} -o {self.__tmpdir} portage')

            self.move_finished(dest=target_dest)

        elif self.__mode == '4':
            # portage_world
            target_dest = Path() / self.__backup_dir / 'world' / self.__date

            os.chdir('/var/lib/portage')
            utils.run_cmd(f'mkzst {self.__verbose} -o {self.__tmpdir} world')

            self.move_finished(dest=target_dest)

        elif self.__mode == '5':
            # all
            utils.run_cmd(f'{utils.get_script_name()} -m 1')
            utils.run_cmd(f'{utils.get_script_name()} -m 2')
            utils.run_cmd(f'{utils.get_script_name()} -m 3')
            utils.run_cmd(f'{utils.get_script_name()} -m 4')

    def run(self, args):
        if args.verbose:
            self.__verbose = '-v'
        if args.user:
            self.__user = args.user
        if args.mode:
            self.__mode = args.mode

        self.backup()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        metavar='EX',
                        nargs='*',
                        help='verbose tar')
    parser.add_argument('-u', '--user',
                        metavar='USER',
                        default='brandon',
                        help='user')
    parser.add_argument('-m', '--mode',
                        metavar='MODE',
                        default=3,
                        choices=['1', '2', '3', '4', '5'],
                        help='Selects backup to run',)
    args = parser.parse_args()

    utils.root_check(require_root=True)

    run = Backup()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
