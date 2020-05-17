#!/usr/bin/env python3
# 1.0.0
# 2020-05-17

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
from pathlib import Path

from utils import utils


class Compress:
    def __init__(self):
        atexit.register(self.remove_tmpdir)
        self.__tmpdir = tempfile.mkdtemp()

        self.__input_files = None
        self.__output_dir = Path.cwd()

        self.__compressing_dir = True

        self.__directories = False
        self.__files = False

        self.__run_tests = True
        self.__file_list = []

        self.__junk_paths = '--junk-paths'

        self.__destructive = False

    def remove_tmpdir(self):
        shutil.rmtree(self.__tmpdir)

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
                utils.run_cmd(f'mk7z -T "{f}"')

    def compress(self, file):
        file = Path(file).name
        print(f'{self.__output_dir}/{file}.zip')
        if Path.exists(Path(f'{self.__output_dir}/{file}.zip')):
            print(f'Skipping, archive already exists at \'{self.__output_dir}/{file}.zip\'')
            return

        self.__file_list.append(f'{self.__output_dir}/{file}.zip')

        os.chdir(Path(file).parent)

        utils.run_cmd(f'nice -19 zip -rv -9 {self.__junk_paths} "{self.__output_dir}/{file}.zip" "{file}"')

        if self.__destructive:
            if self.__compressing_dir:
                shutil.rmtree(file)
            else:
                Path.unlink(file)

    def run(self, args):
        # compression type
        if args.directories:
            self.__directories = True
        if args.files:
            self.__files = True
        # destructive
        if args.no_junk_paths:
            self.__junk_paths = ''
        if args.destructive:
            self.__destructive = True
        # other
        if args.input_files is not None:
            self.__input_files = args.input_files
        if args.diable_tests:
            self.__run_tests = False
        if args.output_dir:
            out = Path.resolve(Path(args.output_dir))
            if not Path.is_dir(out):
                if Path.exists(out):
                    utils.die(msg=f'selected output dir \'{out}\' exists but is not a directory')
                Path(out).mkdir(parents=True, exist_ok=True)
            self.__output_dir = out

        self.get_files()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_files',
                        action='store',
                        type=str,
                        nargs='*',
                        default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument('-P', '--disable-tests',
                        action='store_true',
                        help='disable post compression test')
    parser.add_argument('-o', '--output-dir',
                        metavar='DIR',
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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
