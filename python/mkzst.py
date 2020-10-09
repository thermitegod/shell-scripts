#!/usr/bin/env python3
# 2.10.1
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

# changes should be disseminated to the following scripts when applicable
# mktar
# mkzst
# mkzip
# mk7z
# these are based on each other but different enough that they
# are separated into unique scripts

import argparse
import atexit
import os
import shutil
import tempfile
from pathlib import Path

from utils import utils


class Compress:
    def __init__(self):
        atexit.register(self.remove_tmpdir)
        self.__tmpdir = tempfile.mkdtemp()

        self.__cmd = None
        self.__ext = None

        self.__input_files = None
        self.__output_dir = Path.cwd()

        self.__ultra = False

        self.__exclude = ''

        self.__compressing_dir = True

        self.__directories = False
        self.__files = False
        self.__status = False

        self.__tar_verbose = ''

        self.__destructive = False

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

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

    def get_files(self):
        if self.__directories or self.__files:
            dir_listing = []
            for f in Path(Path.cwd()).iterdir():
                dir_listing.append(f)

            for f in dir_listing:
                if Path.is_dir(f) and self.__directories:
                    self.__compressing_dir = True
                    self.compress(file=f)
                elif Path.is_file(f) and self.__files:
                    self.__compressing_dir = False
                    self.compress(file=f)
        elif self.__input_files is not None:
            for f in self.__input_files:
                f = Path(f)
                if Path.is_dir(f):
                    self.__compressing_dir = True
                    self.compress(file=f)
                elif Path.is_file(f):
                    self.__compressing_dir = False
                    self.compress(file=f)

    def compress(self, file):
        if self.__compressing_dir:
            test_file = Path() / self.__output_dir / f'{file}.tar.{self.__ext}'
        else:
            test_file = Path() / self.__output_dir / f'{file}.{self.__ext}'

        if Path.exists(test_file):
            print(f'Skipping, archive already exists at: \'{test_file}\'')
            return

        script = Path() / self.__tmpdir / 'tmp.sh'
        die = f'die "Compression failed for \'{Path.resolve(file)}\'"'

        os.chdir(Path(file).parent)

        if self.__compressing_dir:
            text = f'tar {self.__exclude} --xattrs -{self.__tar_verbose}Scf - "{Path(file).name}" -P | '
            if self.__status:
                text += f'pv -s "$(du -sb "{Path.resolve(file)}" | awk \'{{print $1}}\')" | '
            text += f'{self.__cmd} >| "{self.__output_dir}/{Path(file).name}.tar.{self.__ext}" || {die}'
        else:
            text = f'{self.__cmd} --output-dir-flat="{self.__output_dir}" -- "{file}" || {die}'

        utils.write_script_shell(script, text)
        utils.run_cmd(script)
        Path.unlink(Path(script))

        if Path.exists(test_file):
            if self.__destructive:
                if self.__compressing_dir:
                    shutil.rmtree(file)
                else:
                    Path.unlink(file)
        else:
            print(f'ERROR: archive not created for: \'{file}\'')
            raise SystemExit(1)

    def run(self, args):
        # compression type
        if args.directories:
            self.__directories = True
        if args.files:
            self.__files = True
        if args.status:
            self.__status = True
        if args.ultra:
            self.__ultra = True
        # destructive
        if args.destructive:
            self.__destructive = True
        # other
        if args.input_files is not None:
            self.__input_files = args.input_files
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
        self.get_files()


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
