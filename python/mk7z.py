# -*- coding: utf-8 -*-
# 2.7.0
# 2021-01-01

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
import re
from pathlib import Path

from python.utils.check_env import CheckEnv
from python.utils.colors import Colors
from python.utils.execute import Execute
from python.utils.get_files import GetFiles
from python.utils.output_dir import OutputDir
from python.utils.script import ExecuteScript


class Compress:
    def __init__(self):
        self.__output_dir = Path.cwd()

        self.__exclude = ''

        self.__run_tests = True
        self.__file_list = []

        self.__destructive = False

        self.__threads = 'on'

        self.__test_move_failed_file = True
        self.__test_passed = 0
        self.__test_failed = 0

    @staticmethod
    def shell_escape(string: str):
        # to get full shell escape have to use .replace because re.escape will not
        # escape single quotes
        return re.escape(string).replace("'", r"\'")

    def test_archive(self, filename):
        filename = Path(filename)
        if Path.is_file(filename) and str(filename).endswith(('.7z', '.zip')):
            print(f'\r{Colors.YEL}TEST{Colors.NC}\t{filename}', end='')

            # have to use shell_escape because syntax gets fucked up with when using sh_wrap=True.
            # double quotes dont work around filename becuse sh_wrap will provide its own double
            # quotes. this is the cleanest solution for dealing with garbage filenames other than
            # renaming them
            status = Execute(f'nice -19 7z t -- {self.shell_escape(str(filename))} | grep Ok',
                             sh_wrap=True, to_stdout=True).get_out()

            if 'Everything is Ok' in status:
                print(f'\r{Colors.GRE}PASSED{Colors.NC}\t{filename}')
                self.__test_passed += 1
            else:
                print(f'\r{Colors.RED}FAILED{Colors.NC}\t{filename}')
                self.__test_failed += 1

                if self.__test_move_failed_file:
                    failed_dir = Path() / filename.parent / 'mk7z-failed'
                    failed_dir.mkdir(parents=True, exist_ok=True)
                    Path.rename(filename, Path() / failed_dir / filename)

    def test_print_results(self):
        total = self.__test_passed + self.__test_failed
        if total != 0:
            print(f'\n\n{Colors.YEL}TOTAL{Colors.NC}\t{total}')
            if self.__test_passed != 0:
                print(f'{Colors.GRE}PASSED{Colors.NC}\t{self.__test_passed}')
            if self.__test_failed != 0:
                print(f'{Colors.RED}FAILED{Colors.NC}\t{self.__test_failed}')

    def run_tests(self):
        if self.__run_tests:
            for f in self.__file_list:
                self.test_archive(filename=f)
            self.test_print_results()

    def compress(self, filename, compressing_dir):
        test_file = Path() / self.__output_dir / f'{filename}.7z'
        if Path.exists(test_file):
            print(f'Skipping, archive already exists at: \'{test_file}\'')
            return

        self.__file_list.append(f'{self.__output_dir}/{Path(filename).name}.7z')

        os.chdir(Path(filename).parent)

        text = f'nice -19 ' \
               f'7zr a -t7z -m0=lzma2 -md=1024m -mmf=bt4 -mmt={self.__threads} -mmtf={self.__threads} ' \
               f'-myx=9 -mx=9 -mfb=276 -mhc=on -ms=on -mtm=off -mtc=off -mta=off {self.__exclude}' \
               f'-o="{self.__output_dir}" "{Path(filename).name}.7z" "{Path(filename).name}" || ' \
               f'die "Compression failed for \'{Path.resolve(filename)}\'"'

        ExecuteScript(text)

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
        # other
        if args.disable_tests:
            self.__run_tests = False
        if args.output_dir:
            self.__output_dir = OutputDir(directory=args.output_dir).get_dir()
        # profile
        if args.single:
            self.__threads = 'off'
        if args.multi:
            self.__threads = 'on'
        # tests
        if args.test:
            for f in args.input_files:
                self.test_archive(filename=f)
            self.test_print_results()
            raise SystemExit
        # destructive
        if args.destructive:
            self.__destructive = True
        if args.exclude:
            for e in args.exclude:
                self.__exclude += f'-x "{e}" '

        GetFiles(function=self.compress, input_files=args.input_files,
                 only_directories=args.directories, only_files=args.files)

        self.run_tests()


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
                        nargs=1,
                        help='create the archive[s] in this directory')
    profile = parser.add_argument_group('profile')
    profile.add_argument('-S', '--single',
                         action='store_true',
                         help='Single threaded, useful when hitting oom with multi')
    profile.add_argument('-M', '--multi',
                         action='store_true',
                         help='Multithreaded [default]')
    batch = parser.add_argument_group('batch creation')
    batch.add_argument('-d', '--directories',
                       action='store_true',
                       help='compress all directories in cwd')
    batch.add_argument('-f', '--files',
                       action='store_true',
                       help='compress all files in cwd')
    other = parser.add_argument_group('other')
    other.add_argument('-T', '-t', '--test',
                       action='store_true',
                       help='Test file[s] passed in $1')
    rm = parser.add_argument_group('destructive')
    rm.add_argument('-z', '--destructive',
                    action='store_true',
                    help='Delete original after it is compressed')
    args = parser.parse_args()

    CheckEnv.args_required_else_help()

    run = Compress()
    run.run(args)
