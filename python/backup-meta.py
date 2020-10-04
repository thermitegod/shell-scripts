#!/usr/bin/env python3
# 1.1.0
# 2020-10-04

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
import sys
import tempfile
import time
from pathlib import Path

from utils import dirs
from utils import utils


class Backup:
    def __init__(self):
        atexit.register(self.remove_tmpdir)
        self.__tmpdir = tempfile.mkdtemp()

        self.__verbose = ''

        self.__backup_dir = Path() / '/mnt/data/backup'

        self.__mode = utils.get_script_name()

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
        if self.__mode == 'backup-chromium':
            target_source = Path() / dirs.get_config_dir() / 'chrome'
            target_dest = Path() / self.__backup_dir / self.__user / 'chromium-profiles' / self.__date

            os.chdir(target_source)
            for f in Path.cwd().iterdir():
                if f.is_dir():
                    utils.run_cmd(f'mkzst --exclude "{f.name}/Default/File System" '
                                  f'{self.__verbose} -o {self.__tmpdir} {f.name}')

            self.move_finished(dest=target_dest)

        elif self.__mode == 'backup-user-bin':
            target_dest = Path() / self.__backup_dir / self.__user / 'bin' / self.__date

            os.chdir(Path.home())
            utils.run_cmd(f'mkzst {self.__verbose} -o {self.__tmpdir} ".bin"')

            self.move_finished(dest=target_dest)

        elif self.__mode == 'backup-user-config':
            target_dest = Path() / self.__backup_dir / self.__user / 'config' / self.__date

            os.chdir(Path.home())
            utils.run_cmd(f'mkzst --exclude ".config/*chrom*" '
                          f'".config/rtorrent/session" '
                          f'".config/transmission/resume" '
                          f'".config/transmission/torrents" '
                          f'{self.__verbose} -o {self.__tmpdir} ".config"')

            self.move_finished(dest=target_dest)

        elif self.__mode == 'backup-user-local':
            target_dest = Path() / self.__backup_dir / self.__user / 'local' / self.__date

            os.chdir(Path.home())
            utils.run_cmd(f'mkzst --exclude ".local/share/Trash" '
                          f'{self.__verbose} -o {self.__tmpdir} ".local"')

            self.move_finished(dest=target_dest)

        elif self.__mode == 'backup-meta':
            utils.run_cmd(f'{sys.argv[0]} -h')
            raise SystemExit

    def run(self, args):
        if args.verbose:
            self.__verbose = '-v'
        if args.user:
            self.__user = args.user

        self.backup()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        metavar='EX',
                        type=str,
                        nargs='*',
                        help='verbose tar')
    parser.add_argument('-u', '--user',
                        metavar='USER',
                        default='brandon',
                        type=str,
                        nargs=1,
                        help='user')
    args = parser.parse_args()

    run = Backup()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
