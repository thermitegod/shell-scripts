# -*- coding: utf-8 -*-
# 2.3.0
# 2020-11-12

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

from python.utils import utils
from python.utils.get_files import GetFiles
from python.utils.output_dir import OutputDir


class Compress:
    def __init__(self):
        self.__output_dir = Path.cwd()

        self.__exclude = ''

        self.__run_tests = True
        self.__file_list = []

        self.__junk_paths = '--junk-paths'

        self.__destructive = False

    def run_tests(self):
        if self.__run_tests:
            for f in self.__file_list:
                utils.run_cmd(f'mk7z -T "{f}"')

    def compress(self, filename, compressing_dir):
        filename = Path(filename).name
        test_file = Path() / self.__output_dir / f'{filename}.zip'
        if Path.exists(test_file):
            print(f'Skipping, archive already exists at: \'{test_file}\'')
            return

        self.__file_list.append(f'{self.__output_dir}/{filename}.zip')

        os.chdir(Path(filename).parent)

        utils.run_cmd(f'nice -19 zip {self.__exclude} -rv -9 '
                      f'{self.__junk_paths} "{self.__output_dir}/{filename}.zip" "{filename}"')

        if Path.exists(test_file):
            if self.__destructive:
                if compressing_dir:
                    shutil.rmtree(filename)
                else:
                    Path.unlink(Path(filename))
        else:
            print(f'ERROR: archive not created for: \'{filename}\'')
            raise SystemExit(1)

    def run(self, args):
        # destructive
        if args.no_junk_paths:
            self.__junk_paths = ''
        if args.destructive:
            self.__destructive = True
        # other
        if args.disable_tests:
            self.__run_tests = False
        if args.output_dir:
            self.__output_dir = OutputDir.set_output_dir(directory=args.output_dir)
        if args.exclude:
            for e in args.exclude:
                self.__exclude += f'--exclude="{e}" '

        GetFiles.get_files(function=self.compress, input_files=args.input_files,
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
    batch = parser.add_argument_group('BATCH CREATION')
    batch.add_argument('-d', '--directories',
                       action='store_true',
                       help='compress all directories in cwd')
    batch.add_argument('-f', '--files',
                       action='store_true',
                       help='compress all files in cwd')
    rm = parser.add_argument_group('DESTRUCTIVE')
    rm.add_argument('-j', '--no-junk-paths',
                    action='store_true',
                    help='do not run zip with \'--junk-paths\'')
    rm.add_argument('-z', '--destructive',
                    action='store_true',
                    help='Delete original after it is compressed')
    args = parser.parse_args()

    utils.args_required_else_help()

    run = Compress()
    run.run(args)
