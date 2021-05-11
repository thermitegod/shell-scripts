# -*- coding: utf-8 -*-
# 1.8.0
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

from python.utils import confirm
from python.utils.execute import Execute
from python.utils.root_check import RootCheck


class Backup:
    def __init__(self, args: argparse = None):
        atexit.register(self.remove_tmpdir)
        self.__tmpdir = Path(tempfile.mkdtemp())

        self.__mtimdb = Path('/var/cache/edb/mtimedb')
        self.__backup_dir = Path('/mnt/data/backup/mtimedb')

        self.parse_args(args=args)

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

    def backup(self):
        Execute(f'mkzst -o {self.__backup_dir} {self.__mtimdb}')
        Path.rename(self.__backup_dir / 'mtimedb.zst', self.__backup_dir / f'mtimedb-{int(time.time())}.zst')

    def list(self):
        if not Path.exists(self.__backup_dir):
            print('Run a backup first')
            raise SystemExit(1)
        Execute(f'ls -1A {self.__backup_dir}')

    def restore(self):
        RootCheck(require_root=True)
        self.list()
        file = input('Enter file to restore: ')
        shutil.copyfile(self.__backup_dir / file, self.__tmpdir / 'mtimedb.zst')
        os.chdir(self.__tmpdir)
        Execute(f'unzstd --long=31 mtimedb.zst')
        if Path.exists(self.__mtimdb):
            Path.unlink(self.__mtimdb)
        shutil.copyfile(self.__tmpdir / 'mtimedb', self.__mtimdb)

    def remove(self):
        if Path.is_dir(self.__backup_dir):
            if confirm.confirm_run(text=f'Remove \'{self.__backup_dir}\'? '):
                shutil.rmtree(self.__backup_dir)

    def parse_args(self, args):
        if args.backup:
            self.backup()
        if args.list:
            self.list()
        if args.restore:
            self.restore()
        if args.remove:
            self.remove()


def main():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required exclusive arguments').add_mutually_exclusive_group(required=True)
    required.add_argument('-b', '--backup',
                          action='store_true',
                          help='backup mtimdb')
    required.add_argument('-s', '--restore',
                          action='store_true',
                          help='retore backuped mtimdb')
    required.add_argument('-l', '--list',
                          action='store_true',
                          help='list backuped mtimdb')
    required.add_argument('-r', '--remove',
                          action='store_true',
                          help='remove backuped mtimdb')
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
