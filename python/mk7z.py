#!/usr/bin/env python3
# 1.8.0
# 2020-10-28

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

from utils import colors
from utils import utils
from utils.script import Script


class Compress:
    def __init__(self):
        self.__input_files = None
        self.__output_dir = Path.cwd()

        self.__compressing_dir = True

        self.__exclude = ''

        self.__directories = False
        self.__files = False

        self.__run_tests = True
        self.__file_list = []

        self.__destructive = False

        self.__threads = 'on'

        self.__test_move_failed_file = True
        self.__test_passed = 0
        self.__test_failed = 0

    def test_archive(self, filename):
        filename = Path(filename)
        c = colors.Colors
        if Path.is_file(filename) and str(filename).endswith(('.7z', '.zip')):
            print(f'\r{c.YEL}TEST{c.NC}\t{filename}', end='')

            # have to use shell_escape because syntax gets fucked up with when using sh_wrap=True.
            # double quotes dont work around filename becuse sh_wrap will provide its own double
            # quotes. this is the cleanest solution for dealing with garbage filenames other than
            # renaming them
            status = utils.run_cmd(f'nice -19 7z t -- {utils.shell_escape(str(filename))} | grep Ok',
                                   sh_wrap=True, to_stdout=True)

            if 'Everything is Ok' in status:
                print(f'\r{c.GRE}PASSED{c.NC}\t{filename}')
                self.__test_passed += 1
            else:
                print(f'\r{c.RED}FAILED{c.NC}\t{filename}')
                self.__test_failed += 1

                if self.__test_move_failed_file:
                    failed_dir = Path() / filename.parent / 'mk7z-failed'
                    failed_dir.mkdir(parents=True, exist_ok=True)
                    Path.rename(filename, Path() / failed_dir / filename)

    def test_print_results(self):
        c = colors.Colors
        total = self.__test_passed + self.__test_failed
        if total != 0:
            print(f'\n\n{c.YEL}TOTAL{c.NC}\t{total}')
            if self.__test_passed != 0:
                print(f'{c.GRE}PASSED{c.NC}\t{self.__test_passed}')
            if self.__test_failed != 0:
                print(f'{c.RED}FAILED{c.NC}\t{self.__test_failed}')

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

        if self.__run_tests:
            for f in self.__file_list:
                self.test_archive(filename=f)
            self.test_print_results()

    def compress(self, file):
        test_file = Path() / self.__output_dir / f'{file}.7z'
        if Path.exists(test_file):
            print(f'Skipping, archive already exists at: \'{test_file}\'')
            return

        self.__file_list.append(f'{self.__output_dir}/{Path(file).name}.7z')

        os.chdir(Path(file).parent)

        text = f'nice -19 ' \
               f'7zr a -t7z -m0=lzma2 -md=1024m -mmf=bt4 -mmt={self.__threads} -mmtf={self.__threads} ' \
               f'-myx=9 -mx=9 -mfb=276 -mhc=on -ms=on -mtm=off -mtc=off -mta=off {self.__exclude}' \
               f'-o="{self.__output_dir}" "{Path(file).name}.7z" "{Path(file).name}" || ' \
               f'die "Compression failed for \'{Path.resolve(file)}\'"'

        Script.execute_script_shell(text=text)

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
        # other
        if args.input_files is not None:
            self.__input_files = args.input_files
        if args.disable_tests:
            self.__run_tests = False
        if args.output_dir:
            out = Path.resolve(Path(args.output_dir[0]))
            if not Path.is_dir(out):
                if Path.exists(out):
                    print(f'selected output dir \'{out}\' exists but is not a directory')
                    raise SystemExit(1)
                Path(out).mkdir(parents=True, exist_ok=True)
            self.__output_dir = out
        # compression type
        if args.directories:
            self.__directories = True
        if args.files:
            self.__files = True
        # profile
        if args.single:
            self.__threads = 'off'
        if args.multi:
            self.__threads = 'on'
        # tests
        if args.test:
            for f in self.__input_files:
                self.test_archive(filename=f)
            self.test_print_results()
            raise SystemExit
        # destructive
        if args.destructive:
            self.__destructive = True
        if args.exclude:
            for e in args.exclude:
                self.__exclude += f'-x "{e}" '

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
                        type=list,
                        nargs='*',
                        help='exclude files from archive')
    parser.add_argument('-P', '--disable-tests',
                        action='store_true',
                        help='disable post compression test')
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
                        type=list,
                        nargs=1,
                        help='create the archive[s] in this directory')
    profile = parser.add_argument_group('PROFILE')
    profile.add_argument('-S', '--single',
                         action='store_true',
                         help='Single threaded, useful when hitting oom with multi')
    profile.add_argument('-M', '--multi',
                         action='store_true',
                         help='Multithreaded [default]')
    batch = parser.add_argument_group('BATCH CREATION')
    batch.add_argument('-d', '--directories',
                       action='store_true',
                       help='compress all directories in cwd')
    batch.add_argument('-f', '--files',
                       action='store_true',
                       help='compress all files in cwd')
    other = parser.add_argument_group('OTHER')
    other.add_argument('-T', '-t', '--test',
                       action='store_true',
                       help='Test file[s] passed in $1')
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
