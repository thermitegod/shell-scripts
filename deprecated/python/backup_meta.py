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
# 1.6.0
# 2021-04-29


import argparse
import atexit
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

from loguru import logger

from utils import dirs
from utils.check_env import CheckEnv
from utils.execute import Execute


class Backup:
    def __init__(self, args: argparse = None):
        atexit.register(self.remove_tmpdir)
        self.__tmpdir = tempfile.mkdtemp()

        self.__verbose = ''

        self.__backup_dir = Path() / '/mnt/data/backup'

        self.__mode = CheckEnv.get_script_name()

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
        if self.__mode == 'backup-chromium':
            target_source = Path() / dirs.get_config_dir() / 'chrome'
            target_dest = Path() / self.__backup_dir / self.__user / 'chromium-profiles' / self.__date

            os.chdir(target_source)
            for f in Path.cwd().iterdir():
                if f.is_dir():
                    Execute(f'mkzst --exclude "{f.name}/Default/File System" '
                            f'{self.__verbose} -o {self.__tmpdir} {f.name}')

            self.move_finished(dest=target_dest)

        elif self.__mode == 'backup-user-bin':
            target_dest = Path() / self.__backup_dir / self.__user / 'bin' / self.__date

            os.chdir(Path.home())
            Execute(f'mkzst {self.__verbose} -o {self.__tmpdir} ".bin"')

            self.move_finished(dest=target_dest)

        elif self.__mode == 'backup-user-config':
            target_dest = Path() / self.__backup_dir / self.__user / 'config' / self.__date

            os.chdir(Path.home())
            Execute(f'mkzst --exclude ".config/*chrom*" '
                    f'".config/rtorrent/session" '
                    f'".config/transmission/resume" '
                    f'".config/transmission/torrents" '
                    f'{self.__verbose} -o {self.__tmpdir} ".config"')

            self.move_finished(dest=target_dest)

        elif self.__mode == 'backup-user-local':
            target_dest = Path() / self.__backup_dir / self.__user / 'local' / self.__date

            os.chdir(Path.home())
            Execute(f'mkzst --exclude ".local/share/Trash" '
                    f'{self.__verbose} -o {self.__tmpdir} ".local"')

            self.move_finished(dest=target_dest)

        elif self.__mode == 'backup-meta':
            Execute(f'{sys.argv[0]} -h')
            raise SystemExit

    def parse_args(self, args):
        if args.verbose:
            self.__verbose = '-v'
        if args.user:
            self.__user = args.user


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='verbose tar')
    parser.add_argument('-u', '--user',
                        metavar='USER',
                        default='brandon',
                        help='user')
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

    Backup(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
