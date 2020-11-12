#!/usr/bin/env python3
# 3.0.0
# 2020-11-11

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
from pathlib import Path

from utils import utils
from utils.get_files import GetFiles
from utils.script import Script


class Compress:
    def __init__(self):
        self.__cmd = None
        self.__ext = None

        self.__output_dir = Path.cwd()

        self.__ultra = False

        self.__exclude = ''

        self.__status = False

        self.__tar_verbose = ''

        self.__destructive = False

    def get_mode(self):
        mode = utils.get_script_name()
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

        os.chdir(Path(filename).parent)

        if compressing_dir:
            text = f'tar {self.__exclude} --xattrs -{self.__tar_verbose}Scf - "{Path(filename).name}" -P | '
            if self.__status:
                text += f'pv -s "$(du -sb "{Path.resolve(filename)}" | awk \'{{print $1}}\')" | '
            text += f'{self.__cmd} >| "{self.__output_dir}/{Path(filename).name}.tar.{self.__ext}" || {die}'
        else:
            text = f'{self.__cmd} --output-dir-flat="{self.__output_dir}" -- "{filename}" || {die}'

        Script.execute_script_shell(text=text)

        if Path.exists(test_file):
            if self.__destructive:
                if compressing_dir:
                    shutil.rmtree(filename)
                else:
                    Path.unlink(filename)
        else:
            print(f'ERROR: archive not created for: \'{filename}\'')
            raise SystemExit(1)

    def run(self, args):
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
            out = Path.resolve(Path(args.output_dir[0]))
            if not Path.is_dir(out):
                if Path.exists(out):
                    print(f'selected output dir \'{out}\' exists but is not a directory')
                    raise SystemExit(1)
                Path(out).mkdir(parents=True, exist_ok=True)
            self.__output_dir = out
        if args.verbose:
            self.__tar_verbose = 'v'
        if args.exclude:
            for e in args.exclude:
                self.__exclude += f'--exclude="{e}" '

        self.get_mode()

        GetFiles.get_files(function=self.compress, input_files=args.input_files,
                           only_directories=args.directories, only_files=args.files)


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
                        type=list,
                        nargs=1,
                        help='create the archive[s] in this directory')
    batch = parser.add_argument_group('BATCH CREATION')
    batch.add_argument('-d', '--directories',
                       action='store_true',
                       help='compress all directories in cwd')
    batch.add_argument('-f', '--files',
                       action='store_true',
                       help='compress all files in cwd')
    rm = parser.add_argument_group('DESTRUCTIVE')
    rm.add_argument('-z', '--destructive',
                    action='store_true',
                    help='Delete original after it is compressed')
    args = parser.parse_args()

    utils.args_required_else_help()

    run = Compress()
    run.run(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit
