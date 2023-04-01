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
# 3.11.0
# 2023-03-31


# changes should be disseminated to the following scripts when applicable
# mktar
# mkzst
# mkzip
# mk7z
# these are based on each other but different enough that they
# are separated into unique scripts

import argparse
import os
import shutil
import sys
from pathlib import Path

from loguru import logger

from utils.archive_utils import RemoveJunk
from utils.check_env import CheckEnv
from utils.get_files import GetFiles
from utils.output_dir import OutputDir
from utils.script import ExecuteBashScript


class Compress:
    def __init__(self, args: argparse = None):
        self.__cmd = None
        self.__ext = None

        self.__output_dir = Path.cwd()

        self.__input_files = None
        self.__directories = False
        self.__files = False

        self.__ultra = False

        self.__exclude = ''

        self.__status = False

        self.__tar_verbose = ''

        self.__destructive = False

        self.parse_args(args=args)

        self.get_mode()

        GetFiles(function=self.compress, input_files=self.__input_files,
                 only_directories=self.__directories, only_files=self.__files)

    def get_mode(self):
        mode = CheckEnv.get_script_name()
        if 'zst' in mode:
            if self.__ultra:
                self.__cmd = 'zstd -T0 --ultra -22 --long=31'
            else:
                self.__cmd = 'zstd -T0 -6 --long=31'
            self.__ext = 'zst'
        elif 'lz4' in mode:
            self.__cmd = 'zstd --format=lz4 -12'
            self.__ext = 'lz4'
        elif 'xz' in mode:
            self.__cmd = 'zstd --format=xz -9'
            self.__ext = 'xz'
        elif 'gz' in mode:
            self.__cmd = 'zstd --format=gzip -9'
            self.__ext = 'gz'

    def compress(self, filename, compressing_dir):
        if compressing_dir:
            test_file = Path() / self.__output_dir / f'{filename}.tar.{self.__ext}'
        else:
            test_file = Path() / self.__output_dir / f'{filename}.{self.__ext}'

        if Path.exists(test_file):
            print(f'Skipping, archive already exists at: \'{test_file}\'')
            return

        die = f'die "Compression failed for \'{Path.resolve(filename)}\'"'

        RemoveJunk(Path(filename))

        os.chdir(Path(filename).parent)

        if compressing_dir:
            text = f'tar {self.__exclude} --xattrs --sort=name -{self.__tar_verbose}cf - "{Path(filename).name}" -P | '
            if self.__status:
                text += f'pv -s "$(du -sb "{Path.resolve(filename)}" | awk \'{{print $1}}\')" | '
            text += f'{self.__cmd} >| "{self.__output_dir}/{Path(filename).name}.tar.{self.__ext}" || {die}'
        else:
            text = f'{self.__cmd} --output-dir-flat="{self.__output_dir}" -- "{filename}" || {die}'

        ExecuteBashScript(text)

        if Path.exists(test_file):
            if self.__destructive:
                if compressing_dir:
                    shutil.rmtree(filename)
                else:
                    Path.unlink(filename)
        else:
            print(f'ERROR: archive not created for: \'{filename}\'')
            raise SystemExit(1)

    def parse_args(self, args):
        # compression type
        if args.status:
            self.__status = True
        if args.ultra:
            self.__ultra = True
        # destructive
        if args.destructive:
            self.__destructive = True
        # other
        if args.output_dir:
            self.__output_dir = OutputDir(directory=args.output_dir).get_dir()
        if args.verbose:
            self.__tar_verbose = 'v'
        if args.exclude:
            for e in args.exclude:
                self.__exclude += f'--exclude="{e}" '

        self.__input_files = args.input_files
        self.__files = args.files
        self.__directories = args.directories


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files',
                        action='store',
                        type=str,
                        nargs='*',
                        default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument('-e', '--exclude',
                        metavar='EX',
                        nargs='*',
                        help='exclude files from archive')
    parser.add_argument('-S', '--status',
                        action='store_true',
                        help='enable cool status bar, directories only')
    parser.add_argument('-u', '--ultra',
                        action='store_true',
                        help='zstd only, create archive wih flags \'--ultra -22\'')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='enable verbose tar')
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        nargs=1,
                        help='create the archive[s] in this directory')
    batch = parser.add_argument_group('batch creation')
    batch.add_argument('-d', '--directories',
                       action='store_true',
                       help='compress all directories in cwd')
    batch.add_argument('-f', '--files',
                       action='store_true',
                       help='compress all files in cwd')
    rm = parser.add_argument_group('destructive')
    rm.add_argument('-z', '--destructive',
                    action='store_true',
                    help='Delete original after it is compressed')
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

    CheckEnv.args_required_else_help()

    Compress(args=args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(1)
